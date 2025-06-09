"""
LLM client for interacting with Ollama language models.
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, Field
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential, 
    retry_if_exception_type, 
    before_sleep_log
)

from .models import LLMModel
from .circuit_breaker import CircuitBreaker
# from .optimized_client import OptimizedLLMClient  # Commented out for now
from core.exceptions.infrastructure import (
    LLMError, 
    ModelNotFoundError, 
    InvalidResponseError, 
    CircuitBreakerOpenError, 
    LLMValidationError, 
    LLMRateLimitError, 
    LLMTimeoutError
)

logger = logging.getLogger(__name__)

@dataclass
class RateLimiter:
    """Rate limiter for LLM API calls."""
    max_requests: int
    time_window: int  # in seconds
    requests: List[float] = None  # timestamps of requests

    def __post_init__(self):
        """Initialize the rate limiter."""
        if self.requests is None:
            self.requests = []

    def can_make_request(self) -> bool:
        """Check if a new request can be made."""
        now = time.time()
        # Remove old requests
        self.requests = [t for t in self.requests
                        if now - t < self.time_window]
        return len(self.requests) < self.max_requests

    def add_request(self):
        """Add a new request timestamp."""
        self.requests.append(time.time())

    def wait_time(self) -> float:
        """Calculate time to wait before next request."""
        if self.can_make_request():
            return 0.0

        now = time.time()
        # Remove old requests
        self.requests = [
            t for t in self.requests if now - t < self.time_window
        ]

        if not self.requests:
            return 0.0

        # Calculate time until oldest request expires
        oldest_request = min(self.requests)
        return max(0.0, oldest_request + self.time_window - now)

class Cache:
    """Cache for API responses."""

    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """Initialize the cache.

        Args:
            max_size: Maximum number of items in cache
            ttl: Time to live in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from cache.

        Args:
            key: Cache key

        Returns:
            Optional[Any]: Cached value if found and not expired, 
                None otherwise
        """
        async with self._lock:
            if key not in self._cache:
                return None

            value, timestamp = self._cache[key]

            # Check if expired
            if datetime.now() - timestamp > timedelta(seconds=self.ttl):
                del self._cache[key]
                return None

            return value

    async def set(self, key: str, value: Any) -> None:
        """Set a value in cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        async with self._lock:
            # Check if cache is full
            if len(self._cache) >= self.max_size:
                # Remove oldest item
                oldest_key = min(
                    self._cache.keys(), 
                    key=lambda k: self._cache[k][1]
)
                del self._cache[oldest_key]

            self._cache[key] = (value, datetime.now())

class LLMResponse(BaseModel):
    """LLM response."""

    text: str = Field(..., description="Response text")
    usage: Dict[str, int] = Field(default_factory=dict, description="Token usage")
    model: str = Field(..., description="Model used")
    created: int = Field(default_factory=lambda: int(time.time()), description="Creation timestamp")

class LLMClient:
    """Client for interacting with Ollama language models."""

    def __init__(
        self, 
        model: str = "llava-phi3", 
        base_url: str = "http://localhost:11434",
        max_tokens: int = 1500,  # Reduced for faster processing
        temperature: float = 0.1,  # Lower for more consistent, faster responses
        cache_ttl: int = 7200,  # 2 hours - longer cache
        rate_limit_requests: int = 50,  # More conservative rate limiting
        rate_limit_period: int = 60,  # 1 minute
        circuit_breaker_failure_threshold: int = 3,  # More aggressive circuit breaking
        circuit_breaker_recovery_timeout: int = 30,  # Faster recovery
        timeout: int = None,  # Auto-configure based on model
        max_retries: int = 2,  # Fewer retries for faster failure handling
        cache_size: int = 2000,  # Larger cache
        keep_alive: bool = True,  # Keep connections alive for performance
        max_concurrent: int = 5  # Limit concurrent requests
):
        """Initialize the Ollama LLM client.

        Args:
            model: Model to use (default: phi)
            base_url: Ollama API base URL
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            cache_ttl: Cache TTL in seconds
            rate_limit_requests: Maximum requests per time window
            rate_limit_period: Time window for rate limiting in seconds
            circuit_breaker_failure_threshold: Number of failures before opening circuit
            circuit_breaker_recovery_timeout: Time to wait before retrying after circuit opens
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            cache_size: Maximum number of items in cache
        """
        self.model = model
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature
        # Auto-configure timeout based on model
        if timeout is None:
            self.timeout = 120 if "llava" in model.lower() else 45  # llava models need more time
        else:
            self.timeout = timeout
        self.max_retries = max_retries

        # Initialize components
        self.cache = Cache(cache_size, cache_ttl)
        self.rate_limiter = RateLimiter(
            max_requests=rate_limit_requests, 
            time_window=rate_limit_period
)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=circuit_breaker_failure_threshold, 
            recovery_timeout=circuit_breaker_recovery_timeout
)

        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=self.timeout  # Use the configured timeout
)

    async def __aenter__(self):
        """Enter async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        await self.client.aclose()

    @lru_cache(maxsize=1000)
    def _get_cache_key(self, prompt: str, **kwargs) -> str:
        """Get cache key."""
        return f"{prompt}:{json.dumps(kwargs, sort_keys=True)}"

    @retry(
        stop=stop_after_attempt(2), 
        wait=wait_exponential(multiplier=0.5, min=2, max=5), 
        retry=retry_if_exception_type((LLMTimeoutError, LLMError)), 
        before_sleep=before_sleep_log(logger, logging.INFO)
)
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None, 
        temperature: Optional[float] = None, 
        max_tokens: Optional[int] = None, 
        cache_key: Optional[str] = None
) -> LLMResponse:
        """Generate text using Ollama with enhanced caching.

        Args:
            prompt: The prompt to generate from
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            cache_key: Optional cache key for response caching

        Returns:
            LLMResponse object containing the generated text

        Raises:
            LLMError: If there's an error with the LLM service
            InvalidResponseError: If the response is invalid
            CircuitBreakerOpenError: If the circuit breaker is open
        """
        # Enhanced caching: Check cache with similarity matching
        if cache_key:
            cached_response = await self.cache.get(cache_key, input_content=prompt)
            if cached_response:
                logger.info(f"🎯 Cache hit for key: {cache_key}")
                return cached_response

        # Check rate limit
        if not self.rate_limiter.can_make_request():
            wait_time = self.rate_limiter.wait_time()
            logger.warning(f"Rate limit exceeded, waiting {wait_time:.2f} seconds")
            await asyncio.sleep(wait_time)

        # Check circuit breaker
        if not self.circuit_breaker.can_execute():
            raise CircuitBreakerOpenError("Circuit breaker is open")

        try:
            # Prepare full prompt with system message if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"

            # Prepare optimized request for llava-phi3 model
            request_data = {
                "model": self.model, 
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.temperature, 
                    "num_predict": max_tokens or self.max_tokens,
                    "top_k": 40 if "llava" in self.model.lower() else 20,  # llava needs more diversity
                    "top_p": 0.95 if "llava" in self.model.lower() else 0.9,  # Higher for llava
                    "repeat_penalty": 1.05 if "llava" in self.model.lower() else 1.1,  # Lower for llava
                    "num_ctx": 4096 if "llava" in self.model.lower() else 2048,  # Larger context for llava
                    "num_thread": 8 if "llava" in self.model.lower() else 4,  # More threads for larger model
                }
            }

            # Make request
            start_time = time.time()
            response = await self._make_request(request_data)
            end_time = time.time()

            # Process response
            if not response or "response" not in response:
                raise InvalidResponseError("Invalid response format")

            response_text = response["response"].strip()
            if not response_text:
                # Handle empty response more gracefully
                logger.warning("Received empty response from LLM")
                response_text = "No response generated"

            # Create response object
            llm_response = LLMResponse(
                text=response_text,
                model=self.model,
                usage={
                    "prompt_tokens": response.get("prompt_eval_count", 0),
                    "completion_tokens": response.get("eval_count", 0),
                    "total_tokens": response.get("prompt_eval_count", 0) + response.get("eval_count", 0)
                },
                created=int(start_time)
)

            # Cache response with input content for enhanced similarity matching
            if cache_key:
                processing_time = end_time - start_time
                await self.cache.set(cache_key, llm_response, processing_time=processing_time, input_content=prompt)

            # Update rate limiter
            self.rate_limiter.add_request()

            # Update circuit breaker
            self.circuit_breaker.on_success()

            return llm_response

        except Exception as e:
            # Update circuit breaker
            self.circuit_breaker.on_failure()

            if isinstance(e, (LLMError, InvalidResponseError)):
                raise

            raise LLMError(f"Error generating text: {str(e)}")

    async def _make_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Ollama API.

        Args:
            data: Request data

        Returns:
            API response

        Raises:
            LLMError: If there's an error with the request
        """
        try:
            response = await self.client.post("/api/generate", json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ModelNotFoundError(f"Model '{self.model}' not found. Make sure it's downloaded in Ollama.")
            elif e.response.status_code >= 500:
                raise LLMError(f"Ollama server error: {e.response.text}")
            else:
                raise LLMError(f"HTTP error {e.response.status_code}: {e.response.text}")
        except httpx.TimeoutException:
            raise LLMTimeoutError("Request to Ollama timed out")
        except httpx.ConnectError:
            raise LLMError("Cannot connect to Ollama. Make sure Ollama is running on localhost:11434")
        except Exception as e:
            raise LLMError(f"Unexpected error: {str(e)}")

    def clear_cache(self):
        """Clear the response cache."""
        self._cache = {}

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "size": len(self._cache),
            "max_size": self.cache.max_size,
            "ttl": self.cache.ttl
        }

    def get_rate_limit_stats(self) -> Dict[str, Any]:
        """Get rate limit statistics."""
        return {
            "max_requests": self.rate_limiter.max_requests, 
            "time_window": self.rate_limiter.time_window, 
            "current_requests": len(self.rate_limiter.requests), 
            "wait_time": self.rate_limiter.wait_time()
        }

    def get_circuit_breaker_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        return self.circuit_breaker.get_stats()

    async def get_structured_completion(
        self, 
        prompt: str, 
        required_fields: List[str] = None,
        numeric_fields: List[str] = None,
        array_fields: List[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Get a structured JSON completion from the model.

        Args:
            prompt: The prompt to send
            required_fields: List of required fields in the response
            numeric_fields: Fields that should be numeric
            array_fields: Fields that should be arrays
            **kwargs: Additional arguments for generate()

        Returns:
            Dict containing the parsed JSON response

        Raises:
            InvalidResponseError: If response is not valid JSON or missing required fields
        """
        # Add JSON format instruction to prompt
        json_prompt = f"""{prompt}

Please respond with valid JSON only. Do not include any explanations or additional text outside the JSON."""

        response = await self.generate(json_prompt, **kwargs)
        
        try:
            # Try to extract JSON from response
            response_text = response.text.strip()

            # Remove common markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Validate required fields
            if required_fields:
                missing_fields = [field for field in required_fields if field not in result]
                if missing_fields:
                    raise InvalidResponseError(f"Missing required fields: {missing_fields}")
            
            # Convert numeric fields
            if numeric_fields:
                for field in numeric_fields:
                    if field in result and result[field] is not None:
                        try:
                            result[field] = float(result[field]) if '.' in str(result[field]) else int(result[field])
                        except (ValueError, TypeError):
                            result[field] = 0
            
                        # Ensure array fields are lists
            if array_fields:
                for field in array_fields:
                    if field in result and not isinstance(result[field], list):
                        if isinstance(result[field], str):
                            result[field] = [result[field]]
                        else:
                            result[field] = []
            
            return result
            
        except json.JSONDecodeError as e:
            raise InvalidResponseError(f"Invalid JSON response: {str(e)}")
        except Exception as e:
            raise InvalidResponseError(f"Error processing structured response: {str(e)}")

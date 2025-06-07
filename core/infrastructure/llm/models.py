"""
Models for LLM infrastructure.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from dataclasses import dataclass, field
from enum import Enum
from pydantic import BaseModel, Field, validator

class LLMModel(str, Enum):
    """Supported LLM models."""
    GPT4 = "gpt - 4"
    GPT35 = "gpt - 3.5 - turbo"
    CLAUDE = "claude - 3-opus"
    MISTRAL = "mistral - large"
    PHI = "phi"

class LLMResponse(BaseModel):
    """Response from LLM."""
    text: str = Field(..., description="Generated text")
    model: str = Field(..., description="Model used for generation")
    usage: Dict[str, int] = Field(default_factory = dict, description="Token usage statistics")
    finish_reason: Optional[str] = Field(None, description="Reason for finishing generation")
    processing_time: float = Field(..., description="Time taken to process request in seconds")
    created_at: datetime = Field(default_factory = datetime.now, description="When the response was created")

    @validator('text')
    def text_must_not_be_empty(cls, v):
        """Validate that text is not empty."""
        if not v.strip():
            raise ValueError('text must not be empty')
        return v

    @validator('processing_time')
    def processing_time_must_be_positive(cls, v):
        """Validate that processing time is positive."""
        if v <= 0:
            raise ValueError('processing_time must be positive')
        return v

    @validator('usage')
    def validate_usage(cls, v):
        """Validate usage statistics."""
        required_fields = {'prompt_tokens', 'completion_tokens', 'total_tokens'}
        if not all(field in v for field in required_fields):
            raise ValueError(f'usage must contain {required_fields}')
        if not all(isinstance(v[field], int) and v[field] >= 0 for field in required_fields):
            raise ValueError('usage values must be non - negative integers')
        return v

class LLMRequest(BaseModel):
    """Request to LLM."""
    model: LLMModel = Field(..., description="Model to use")
    prompt: str = Field(..., description="Prompt to generate from")
    system_prompt: Optional[str] = Field(None, description="Optional system prompt")
    temperature: float = Field(0.7, ge = 0.0, le = 2.0, description="Temperature for generation")
    max_tokens: int = Field(2000, gt = 0, description="Maximum tokens to generate")
    top_p: float = Field(1.0, ge = 0.0, le = 1.0, description="Top - p sampling parameter")
    top_k: int = Field(40, gt = 0, description="Top - k sampling parameter")
    presence_penalty: float = Field(0.0, ge=-2.0, le = 2.0, description="Presence penalty")
    frequency_penalty: float = Field(0.0, ge=-2.0, le = 2.0, description="Frequency penalty")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")
    stream: bool = Field(False, description="Whether to stream the response")

    @validator('prompt')
    def prompt_must_not_be_empty(cls, v):
        """Validate that prompt is not empty."""
        if not v.strip():
            raise ValueError('prompt must not be empty')
        return v

    @validator('system_prompt')
    def system_prompt_must_not_be_empty(cls, v):
        """Validate that system prompt is not empty if provided."""
        if v is not None and not v.strip():
            raise ValueError('system_prompt must not be empty if provided')
        return v

class LLMConfig(BaseModel):
    """Configuration for LLM client."""
    api_key: str = Field(..., description="API key for LLM service")
    model: LLMModel = Field(LLMModel.GPT4, description="Default model to use")
    max_tokens: int = Field(2000, gt = 0, description="Default maximum tokens")
    temperature: float = Field(0.7, ge = 0.0, le = 2.0, description="Default temperature")
    cache_ttl: int = Field(3600, gt = 0, description="Cache TTL in seconds")
    rate_limit_requests: int = Field(100, gt = 0, description="Maximum requests per time window")
    rate_limit_period: int = Field(60, gt = 0, description="Time window for rate limiting in seconds")
    circuit_breaker_failure_threshold: int = Field(5, gt = 0, description="Number of failures before opening circuit")
    circuit_breaker_recovery_timeout: int = Field(60, gt = 0, description="Time to wait before retrying after circuit opens")
    timeout: int = Field(30, gt = 0, description="Request timeout in seconds")
    max_retries: int = Field(3, gt = 0, description="Maximum number of retries")

    class Config:
        """Pydantic config."""
        use_enum_values = True

class LLMStats(BaseModel):
    """Statistics for LLM client."""
    total_requests: int = Field(0, ge = 0, description="Total number of requests")
    successful_requests: int = Field(0, ge = 0, description="Number of successful requests")
    failed_requests: int = Field(0, ge = 0, description="Number of failed requests")
    total_tokens: int = Field(0, ge = 0, description="Total tokens processed")
    total_processing_time: float = Field(0.0, ge = 0.0, description="Total processing time in seconds")
    cache_hits: int = Field(0, ge = 0, description="Number of cache hits")
    cache_misses: int = Field(0, ge = 0, description="Number of cache misses")
    rate_limit_hits: int = Field(0, ge = 0, description="Number of rate limit hits")
    circuit_breaker_trips: int = Field(0, ge = 0, description="Number of circuit breaker trips")

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests

    @property
    def average_processing_time(self) -> float:
        """Calculate average processing time."""
        if self.total_requests == 0:
            return 0.0
        return self.total_processing_time / self.total_requests

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total_cache_requests = self.cache_hits + self.cache_misses
        if total_cache_requests == 0:
            return 0.0
        return self.cache_hits / total_cache_requests

    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary."""
        return {
            "total_requests": self.total_requests, 
            "successful_requests": self.successful_requests, 
            "failed_requests": self.failed_requests, 
            "success_rate": self.success_rate, 
            "total_tokens": self.total_tokens, 
            "total_processing_time": self.total_processing_time, 
            "average_processing_time": self.average_processing_time, 
            "cache_hits": self.cache_hits, 
            "cache_misses": self.cache_misses, 
            "cache_hit_rate": self.cache_hit_rate, 
            "rate_limit_hits": self.rate_limit_hits, 
            "circuit_breaker_trips": self.circuit_breaker_trips
        }

"""Infrastructure - related exceptions."""

class InfrastructureError(Exception):
    """Base exception for infrastructure - related errors."""
    pass

class LLMError(InfrastructureError):
    """Base exception for LLM - related errors."""
    pass

class ModelNotFoundError(LLMError):
    """Exception raised when a model is not found."""
    pass

class InvalidResponseError(LLMError):
    """Exception raised when an invalid response is received."""
    pass

class CircuitBreakerOpenError(LLMError):
    """Exception raised when circuit breaker is open."""
    pass

class LLMValidationError(LLMError):
    """Exception raised when LLM input validation fails."""
    pass

class LLMRateLimitError(LLMError):
    """Exception raised when rate limit is exceeded."""
    pass

class LLMTimeoutError(LLMError):
    """Exception raised when LLM request times out."""
    pass

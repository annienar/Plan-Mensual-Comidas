"""
LLM exceptions.

This module contains LLM - related exceptions.
"""

from .base import DomainError

class LLMError(DomainError):
    """Base LLM error."""
    pass

class LLMValidationError(LLMError):
    """Validation error."""
    pass

class LLMGenerationError(LLMError):
    """Generation error."""
    pass

class LLMTimeoutError(LLMError):
    """Timeout error."""
    pass

class LLMRateLimitError(LLMError):
    """Rate limit error."""
    pass

"""
Notion exceptions.

This module contains Notion - related exceptions.
"""

from .base import DomainError

class NotionError(DomainError):
    """Base Notion error."""
    pass

class NotionRateLimitError(NotionError):
    """Rate limit error."""
    pass

class NotionTimeoutError(NotionError):
    """Timeout error."""
    pass

class NotionValidationError(NotionError):
    """Validation error."""
    pass

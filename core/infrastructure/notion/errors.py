"""
Exception hierarchy for Notion integration.
"""
from typing import Optional

class NotionError(Exception):
    """Base exception for Notion - related errors."""
    pass

class NotionAPIError(NotionError):
    """Exception raised when there's an error with the Notion API."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[dict] = None) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code if available
            response: API response if available
        """
        super().__init__(message)
        self.status_code = status_code
        self.response = response

class NotionRateLimitError(NotionAPIError):
    """Exception raised when rate limit is exceeded."""
    pass

class NotionAuthenticationError(NotionAPIError):
    """Exception raised when authentication fails."""
    pass

class NotionValidationError(NotionError):
    """Exception raised when input validation fails."""
    pass

class NotionDatabaseError(NotionError):
    """Exception raised when there's an error with a database operation."""
    pass

class NotionPageError(NotionError):
    """Exception raised when there's an error with a page operation."""
    pass

class NotionBlockError(NotionError):
    """Exception raised when there's an error with a block operation."""
    pass

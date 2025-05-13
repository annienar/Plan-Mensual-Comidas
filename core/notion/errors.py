class NotionAPIError(Exception):
    """Raised when a Notion API call fails."""
    pass

class NotionRateLimitError(NotionAPIError):
    """Raised when Notion API rate limits are exceeded."""
    pass

class NotionValidationError(NotionAPIError):
    """Raised when data sent to Notion is invalid."""
    pass 
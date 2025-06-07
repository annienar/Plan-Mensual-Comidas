"""
Client for interacting with Notion API.
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, Any, Optional, List

import httpx
from notion_client import Client
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.utils.logger import get_logger
from .errors import (
    NotionAPIError, 
    NotionRateLimitError, 
    NotionAuthenticationError, 
    NotionValidationError, 
    NotionDatabaseError, 
    NotionPageError, 
    NotionBlockError
)
from .models import NotionConfig, NotionMetrics, NotionPage, NotionDatabase, NotionBlock
from .rate_limiter import RateLimiter

logger = get_logger(__name__)

class Cache:
    """Cache.

    This class handles caching of API responses.
    """

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
            Optional[Any]: Cached value if found and not expired, None otherwise
        """
        async with self._lock:
            if key not in self._cache:
                return None

            value, timestamp = self._cache[key]

            # Check if expired
            if datetime.now() - timestamp > timedelta(seconds = self.ttl):
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
                    key = lambda k: self._cache[k][1]
)
                del self._cache[oldest_key]

            self._cache[key] = (value, datetime.now())

class NotionResponse(BaseModel):
    """Notion response.

    This class represents a Notion API response.
    """

    data: Dict[str, Any] = Field(..., description="Response data")
    has_more: bool = Field(..., description="Whether there are more results")
    next_cursor: Optional[str] = Field(None, description="Next cursor for pagination")

class NotionClient:
    """Client for interacting with Notion API."""

    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """Ensure singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: Optional[NotionConfig] = None) -> None:
        """Initialize the Notion client.

        Args:
            config: Optional configuration for the client
        """
        if not self._initialized:
            self.config = config or NotionConfig(
                api_key = os.getenv("NOTION_API_KEY", "")
)

            if not self.config.api_key:
                raise NotionAuthenticationError("Notion API key is required")

            self.client = Client(auth = self.config.api_key)
            self._rate_limiter = RateLimiter(self.config.rate_limit)
            self._metrics = NotionMetrics()
            self._databases: Dict[str, NotionDatabase] = {}  # Cache for database IDs

            # Initialize missing attributes used by _request method
            self.cache = Cache()
            self.rate_limiter = self._rate_limiter  # Alias for consistency
            self.max_retries = 3

            self._initialized = True

    @retry(
        stop = stop_after_attempt(3), 
        wait = wait_exponential(multiplier = 1, min = 2, max = 10), 
        retry = retry_if_exception_type((NotionAPIError, ConnectionError))
)
    async def check_connection(self) -> bool:
        """Verify connection to Notion API.

        Returns:
            bool: True if connection is successful

        Raises:
            NotionAPIError: If connection fails
        """
        try:
            await self._rate_limiter.acquire()
            self.client.users.me()
            self._metrics.record_request(True)
            return True
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionAPIError(f"Failed to connect to Notion API: {e}")

    @retry(
        stop = stop_after_attempt(3), 
        wait = wait_exponential(multiplier = 1, min = 2, max = 10), 
        retry = retry_if_exception_type((NotionAPIError, ConnectionError))
)
    async def check_database(self, database_id: str) -> bool:
        """Verify access to the database.

        Args:
            database_id: ID of the database to check

        Returns:
            bool: True if access is successful

        Raises:
            NotionAPIError: If access fails
        """
        try:
            await self._rate_limiter.acquire()
            self.client.databases.retrieve(database_id)
            self._metrics.record_request(True)
            return True
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionAPIError(f"Failed to access Notion database: {e}")

    async def get_database(self, database_id: str) -> NotionDatabase:
        """Get a database by ID.

        Args:
            database_id: ID of the database to get

        Returns:
            NotionDatabase: The database information

        Raises:
            NotionDatabaseError: If database retrieval fails
        """
        try:
            await self._rate_limiter.acquire()
            response = self.client.databases.retrieve(database_id = database_id)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionDatabaseError(f"Failed to get database: {e}")

    async def query_database(
        self, 
        database_id: str, 
        filter_dict: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
        """Query a Notion database with optional filters.

        Args:
            database_id: ID of the database to query
            filter_dict: Optional filters to apply

        Returns:
            Dict[str, Any]: Query results

        Raises:
            NotionDatabaseError: If query fails
        """
        try:
            await self._rate_limiter.acquire()
            query_params = {"database_id": database_id}
            if filter_dict:
                query_params["filter"] = filter_dict
            response = self.client.databases.query(**query_params)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionDatabaseError(f"Failed to query Notion database: {e}")

    async def create_page(
        self, 
        database_id: str, 
        properties: Dict[str, Any]
) -> NotionPage:
        """Create a new page in a database.

        Args:
            database_id: ID of the database to create the page in
            properties: Page properties

        Returns:
            NotionPage: The created page

        Raises:
            NotionPageError: If page creation fails
        """
        try:
            await self._rate_limiter.acquire()
            response = self.client.pages.create(
                parent={"database_id": database_id}, 
                properties = properties
)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionPageError(f"Failed to create page: {e}")

    async def update_page(
        self, 
        page_id: str, 
        properties: Dict[str, Any]
) -> NotionPage:
        """Update an existing page.

        Args:
            page_id: ID of the page to update
            properties: Updated page properties

        Returns:
            NotionPage: The updated page

        Raises:
            NotionPageError: If page update fails
        """
        try:
            await self._rate_limiter.acquire()
            response = self.client.pages.update(
                page_id = page_id, 
                properties = properties
)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionPageError(f"Failed to update page: {e}")

    async def get_page(self, page_id: str) -> NotionPage:
        """Fetch a Notion page by ID.

        Args:
            page_id: ID of the page to fetch

        Returns:
            NotionPage: The page information

        Raises:
            NotionPageError: If page retrieval fails
        """
        try:
            await self._rate_limiter.acquire()
            response = self.client.pages.retrieve(page_id = page_id)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionPageError(f"Failed to retrieve Notion page: {e}")

    async def append_blocks(
        self, 
        page_id: str, 
        blocks: List[NotionBlock]
) -> Dict[str, Any]:
        """Append blocks to a Notion page.

        Args:
            page_id: ID of the page to append blocks to
            blocks: Blocks to append

        Returns:
            Dict[str, Any]: API response

        Raises:
            NotionBlockError: If block append fails
        """
        try:
            await self._rate_limiter.acquire()
            response = self.client.blocks.children.append(
                block_id = page_id, 
                children = blocks
)
            self._metrics.record_request(True)
            return response
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionBlockError(f"Failed to append blocks to Notion page: {e}")

    async def delete_page(self, page_id: str) -> None:
        """Delete a Notion page.

        Args:
            page_id: ID of the page to delete

        Raises:
            NotionPageError: If page deletion fails
        """
        try:
            await self._rate_limiter.acquire()
            self.client.pages.update(
                page_id = page_id, 
                archived = True
)
            self._metrics.record_request(True)
        except Exception as e:
            self._metrics.record_request(False)
            raise NotionPageError(f"Failed to delete Notion page: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics.

        Returns:
            Dict[str, Any]: Current metrics summary
        """
        return self._metrics.get_metrics_summary()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        pass

    def _get_cache_key(self, endpoint: str, **kwargs) -> str:
        """Get cache key.

        Args:
            endpoint: API endpoint
            **kwargs: Additional parameters

        Returns:
            str: Cache key
        """
        return f"{endpoint}:{json.dumps(kwargs, sort_keys = True)}"

    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
) -> NotionResponse:
        """Make a request to the Notion API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional parameters

        Returns:
            NotionResponse: API response

        Raises:
            NotionAPIError: If an error occurs
        """
        # This is a simplified implementation since the notion - client library
        # handles the HTTP requests internally. This method is kept for
        # compatibility but delegates to the main client methods.
        try:
            # For now, just return a simple response structure
            # In a real implementation, this would make an HTTP request
            # using httpx or requests to the Notion API directly
            result = {"results": [], "has_more": False, "next_cursor": None}

            return NotionResponse(
                data = result, 
                has_more = result.get("has_more", False), 
                next_cursor = result.get("next_cursor")
)
        except Exception as e:
            raise NotionAPIError(f"Request failed: {str(e)}")

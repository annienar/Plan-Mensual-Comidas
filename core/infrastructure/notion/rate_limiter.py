"""
Rate limiting implementation for Notion API requests.
"""

from core.utils.logger import get_logger
from datetime import datetime, timedelta
from typing import Optional

import asyncio
import time
logger = get_logger(__name__)

class RateLimiter:
    """Rate limiter for Notion API requests."""

    def __init__(self, requests_per_second: int) -> None:
        """Initialize the rate limiter.

        Args:
            requests_per_second: Maximum number of requests per second
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time: Optional[float] = None
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire permission to make a request.

        This method will wait if necessary to respect the rate limit.
        """
        async with self._lock:
            now = time.time()

            if self.last_request_time is not None:
                # Calculate time to wait
                elapsed = now - self.last_request_time
                if elapsed < self.min_interval:
                    wait_time = self.min_interval - elapsed
                    logger.debug(f"Rate limit hit, waiting {wait_time:.2f}s")
                    await asyncio.sleep(wait_time)

            self.last_request_time = time.time()

    def reset(self) -> None:
        """Reset the rate limiter state."""
        self.last_request_time = None

"""
Cache implementation for LLM responses.
"""

from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

from .models import LLMResponse
from dataclasses import dataclass, field
import time
@dataclass

class CacheEntry:
    """Cache entry with TTL."""
    value: Any
    created_at: float = field(default_factory = time.time)
    last_accessed: float = field(default_factory = time.time)
    access_count: int = 0

    def is_expired(self, ttl: float) -> bool:
        """Check if entry is expired.

        Args:
            ttl: Time to live in seconds

        Returns:
            bool: True if entry is expired, False otherwise
        """
        return time.time() - self.created_at > ttl

    def update_access(self) -> None:
        """Update access time and count."""
        self.last_accessed = time.time()
        self.access_count += 1

@dataclass

class CacheStats:
    """Cache statistics."""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    size: int = 0
    max_size: int = 0
    ttl: float = 0

    def hit_rate(self) -> float:
        """Calculate cache hit rate.

        Returns:
            float: Cache hit rate
        """
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary.

        Returns:
            Dict[str, Any]: Cache statistics
        """
        return {
            "hits": self.hits, 
            "misses": self.misses, 
            "evictions": self.evictions, 
            "size": self.size, 
            "max_size": self.max_size, 
            "hit_rate": self.hit_rate(), 
            "ttl": self.ttl
        }

class LLMCache:
    """Cache for LLM responses with TTL and LRU eviction."""

    def __init__(
        self, 
        max_size: int = 1000, 
        ttl: float = 3600.0,  # 1 hour
        cleanup_interval: float = 300.0  # 5 minutes
):
        """Initialize the cache.

        Args:
            max_size: Maximum number of entries
            ttl: Time to live in seconds
            cleanup_interval: Interval for cleanup in seconds
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()

        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._stats = CacheStats(max_size = max_size, ttl = ttl)

    def get(self, key: str) -> Optional[LLMResponse]:
        """Get a value from the cache.

        Args:
            key: Cache key

        Returns:
            Optional[LLMResponse]: Cached value or None if not found / expired
        """
        self._cleanup_if_needed()

        entry = self._cache.get(key)
        if entry is None:
            self._stats.misses += 1
            return None

        if entry.is_expired(self.ttl):
            self._stats.misses += 1
            del self._cache[key]
            self._stats.size -= 1
            return None

        entry.update_access()
        self._cache.move_to_end(key)
        self._stats.hits += 1
        return entry.value

    def set(self, key: str, value: LLMResponse) -> None:
        """Set a value in the cache.

        Args:
            key: Cache key
            value: Value to cache
        """
        self._cleanup_if_needed()

        if key in self._cache:
            # Update existing entry
            entry = self._cache[key]
            entry.value = value
            entry.created_at = time.time()
            entry.update_access()
            self._cache.move_to_end(key)
        else:
            # Add new entry
            if len(self._cache) >= self.max_size:
                # Evict least recently used entry
                self._cache.popitem(last = False)
                self._stats.evictions += 1
                self._stats.size -= 1

            self._cache[key] = CacheEntry(value = value)
            self._stats.size += 1

    def delete(self, key: str) -> bool:
        """Delete a value from the cache.

        Args:
            key: Cache key

        Returns:
            bool: True if key was found and deleted, False otherwise
        """
        if key in self._cache:
            del self._cache[key]
            self._stats.size -= 1
            return True
        return False

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()
        self._stats.size = 0
        self._stats.evictions += len(self._cache)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dict[str, Any]: Cache statistics
        """
        return self._stats.to_dict()

    def _cleanup_if_needed(self) -> None:
        """Clean up expired entries if needed."""
        now = time.time()
        if now - self.last_cleanup < self.cleanup_interval:
            return

        expired_keys = [
            key for key, entry in self._cache.items()
            if entry.is_expired(self.ttl)
        ]

        for key in expired_keys:
            del self._cache[key]
            self._stats.size -= 1

        self.last_cleanup = now

    def get_oldest_entry(self) -> Optional[Tuple[str, CacheEntry]]:
        """Get the oldest entry in the cache.

        Returns:
            Optional[Tuple[str, CacheEntry]]: Oldest entry or None if cache is empty
        """
        if not self._cache:
            return None
        key = next(iter(self._cache))
        return key, self._cache[key]

    def get_newest_entry(self) -> Optional[Tuple[str, CacheEntry]]:
        """Get the newest entry in the cache.

        Returns:
            Optional[Tuple[str, CacheEntry]]: Newest entry or None if cache is empty
        """
        if not self._cache:
            return None
        key = next(reversed(self._cache))
        return key, self._cache[key]

    def get_most_accessed_entry(self) -> Optional[Tuple[str, CacheEntry]]:
        """Get the most accessed entry in the cache.

        Returns:
            Optional[Tuple[str, CacheEntry]]: Most accessed entry or None if cache is empty
        """
        if not self._cache:
            return None
        return max(
            self._cache.items(), 
            key = lambda x: x[1].access_count
)

    def get_least_accessed_entry(self) -> Optional[Tuple[str, CacheEntry]]:
        """Get the least accessed entry in the cache.

        Returns:
            Optional[Tuple[str, CacheEntry]]: Least accessed entry or None if cache is empty
        """
        if not self._cache:
            return None
        return min(
            self._cache.items(), 
            key = lambda x: x[1].access_count
)

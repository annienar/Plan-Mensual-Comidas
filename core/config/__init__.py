"""
Configuration module.

This module handles all configuration - related functionality.
"""

from .loader import ConfigLoader
from .settings import Settings

try:
    config = ConfigLoader().load()
except Exception:
    # Fallback config if loading fails
    from .settings import (
        CacheSettings,
        LLMSettings,
        LoggingSettings,
        NotionSettings,
        PathSettings,
    )

    config = Settings(
        llm=LLMSettings(
            model="phi", temperature=0.7, max_tokens=1000, timeout=30, base_url="http://localhost:11434"
        ),
        notion=NotionSettings(api_key="dummy", database_id="dummy", timeout=30),
        debug=False,
        log_level="INFO",
        PATHS=PathSettings(),
        LOGGING=LoggingSettings(),
        CACHE=CacheSettings(),
    )

__all__ = [
    "Settings",
    "ConfigLoader",
    "config",
]

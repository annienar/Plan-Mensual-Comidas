"""
Configuration loader module.

This module handles loading configuration from various sources.
"""

from pathlib import Path
from typing import Optional
import os

from ..exceptions.config import ConfigError, ConfigNotFoundError
from .settings import Settings, LLMSettings, NotionSettings
from dotenv import load_dotenv


class ConfigLoader:
    """Configuration loader.

    This class handles loading configuration from various sources.
    """

    def __init__(self, env_file: Optional[str] = None):
        """Initialize the loader.

        Args:
            env_file: Path to .env file
        """
        self.env_file = env_file or ".env"

    def load(self) -> Settings:
        """Load configuration.

        Returns:
            Settings: Loaded settings

        Raises:
            ConfigError: If configuration cannot be loaded
        """
        # Load environment variables
        self._load_env()

        # Create settings
        try:
            return Settings(
                llm=self._load_llm_settings(),
                notion=self._load_notion_settings(),
                debug=self._get_bool("DEBUG", False),
                log_level=self._get_str("LOG_LEVEL", "INFO"),
            )
        except Exception as e:
            raise ConfigError(f"Failed to load settings: {e}")

    def _load_env(self) -> None:
        """Load environment variables.

        Raises:
            ConfigNotFoundError: If .env file is not found
        """
        env_path = Path(self.env_file)
        if not env_path.exists():
            raise ConfigNotFoundError(f".env file not found: {self.env_file}")

        load_dotenv(env_path)

    def _load_llm_settings(self) -> LLMSettings:
        """Load LLM settings.

        Returns:
            LLMSettings: LLM settings
        """
        return LLMSettings(
            api_key=self._get_str("OPENAI_API_KEY"),
            model=self._get_str("OPENAI_MODEL", "gpt-4"),
            temperature=self._get_float("OPENAI_TEMPERATURE", 0.7),
            max_tokens=self._get_int("OPENAI_MAX_TOKENS", 1000),
            timeout=self._get_int("OPENAI_TIMEOUT", 30),
        )

    def _load_notion_settings(self) -> NotionSettings:
        """Load Notion settings.

        Returns:
            NotionSettings: Notion settings
        """
        return NotionSettings(
            api_key=self._get_str("NOTION_API_KEY"),
            database_id=self._get_str("NOTION_DATABASE_ID"),
            timeout=self._get_int("NOTION_TIMEOUT", 30),
        )

    def _get_str(self, key: str, default: Optional[str] = None) -> str:
        """Get string value from environment.

        Args:
            key: Environment variable key
            default: Default value

        Returns:
            str: Value

        Raises:
            ConfigError: If value is not found and no default is provided
        """
        value = os.getenv(key, default)
        if value is None:
            raise ConfigError(f"Required environment variable not found: {key}")
        return value

    def _get_int(self, key: str, default: Optional[int] = None) -> int:
        """Get integer value from environment.

        Args:
            key: Environment variable key
            default: Default value

        Returns:
            int: Value

        Raises:
            ConfigError: If value is not found and no default is provided
        """
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ConfigError(f"Required environment variable not found: {key}")

        try:
            return int(value)
        except ValueError:
            raise ConfigError(f"Invalid integer value for {key}: {value}")

    def _get_float(self, key: str, default: Optional[float] = None) -> float:
        """Get float value from environment.

        Args:
            key: Environment variable key
            default: Default value

        Returns:
            float: Value

        Raises:
            ConfigError: If value is not found and no default is provided
        """
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ConfigError(f"Required environment variable not found: {key}")

        try:
            return float(value)
        except ValueError:
            raise ConfigError(f"Invalid float value for {key}: {value}")

    def _get_bool(self, key: str, default: Optional[bool] = None) -> bool:
        """Get boolean value from environment.

        Args:
            key: Environment variable key
            default: Default value

        Returns:
            bool: Value

        Raises:
            ConfigError: If value is not found and no default is provided
        """
        value = os.getenv(key)
        if value is None:
            if default is not None:
                return default
            raise ConfigError(f"Required environment variable not found: {key}")

        return value.lower() in ("true", "1", "yes", "y")

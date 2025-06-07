"""
Settings module.

This module contains the application settings.
"""

from pathlib import Path

from pydantic import BaseModel, Field


class LLMSettings(BaseModel):
    """LLM settings.

    Attributes:
        api_key: OpenAI API key
        model: Model to use
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        timeout: Request timeout in seconds
    """

    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field("gpt - 4", description="Model to use")
    temperature: float = Field(0.7, description="Temperature for generation")
    max_tokens: int = Field(1000, description="Maximum tokens to generate")
    timeout: int = Field(30, description="Request timeout in seconds")


class NotionSettings(BaseModel):
    """Notion settings.

    Attributes:
        api_key: Notion API key
        database_id: Database ID
        timeout: Request timeout in seconds
    """

    api_key: str = Field(..., description="Notion API key")
    database_id: str = Field(..., description="Database ID")
    timeout: int = Field(30, description="Request timeout in seconds")


class PathSettings(BaseModel):
    """Path settings."""

    LOG_DIR: Path = Field(default=Path("var/logs"), description="Log directory")
    TEST_RESULTS_DIR: Path = Field(
        default=Path("var/test-results"), description="Test results directory"
    )
    VAR_DIR: Path = Field(default=Path("var"), description="Variable data directory")


class LoggingSettings(BaseModel):
    """Logging settings."""

    FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log message format",
    )
    DATE_FORMAT: str = Field(default="%Y-%m-%d %H:%M:%S", description="Date format")


class CacheSettings(BaseModel):
    """Cache settings."""

    MAX_SIZE: int = Field(
        default=10485760, description="Max cache size in bytes"
    )  # 10MB
    TTL: int = Field(default=5, description="Cache TTL")


class Settings(BaseModel):
    """Application settings.

    Attributes:
        llm: LLM settings
        notion: Notion settings
        debug: Whether to enable debug mode
        log_level: Logging level
    """

    llm: LLMSettings
    notion: NotionSettings
    debug: bool = Field(False, description="Whether to enable debug mode")
    log_level: str = Field("INFO", description="Logging level")
    PATHS: PathSettings = Field(default_factory=PathSettings)
    LOGGING: LoggingSettings = Field(default_factory=LoggingSettings)
    CACHE: CacheSettings = Field(default_factory=CacheSettings)

    # Application constants
    PROJECT_NAME: str = Field(
        default="Plan Mensual Comidas", description="Project name"
    )
    VERSION: str = Field(default="1.0.0", description="Application version")
    DEFAULT_ENCODING: str = Field(default="utf-8", description="Default encoding")

    # File extensions
    TEXT_EXTENSIONS: list = Field(
        default=[".txt", ".md"], description="Text file extensions"
    )
    PDF_EXTENSIONS: list = Field(default=[".pdf"], description="PDF file extensions")
    IMAGE_EXTENSIONS: list = Field(
        default=[".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        description="Image file extensions",
    )

    def is_supported_extension(self, file_path: Path) -> bool:
        """Check if file extension is supported."""
        extension = file_path.suffix.lower()
        return extension in (
            self.TEXT_EXTENSIONS + self.PDF_EXTENSIONS + self.IMAGE_EXTENSIONS
        )

    def get_file_type(self, file_path: Path) -> str:
        """Get file type based on extension."""
        extension = file_path.suffix.lower()
        if extension in self.TEXT_EXTENSIONS:
            return "text"
        elif extension in self.PDF_EXTENSIONS:
            return "pdf"
        elif extension in self.IMAGE_EXTENSIONS:
            return "image"
        else:
            return "unknown"

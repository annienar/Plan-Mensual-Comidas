"""Configuration - related exceptions."""

class ConfigError(Exception):
    """Base exception for configuration - related errors."""
    pass

class ConfigNotFoundError(ConfigError):
    """Exception raised when configuration is not found."""
    pass

class ConfigValidationError(ConfigError):
    """Exception raised when configuration validation fails."""
    pass

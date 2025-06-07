"""
Logging configuration for the application.
"""

import sys

from .settings import Settings
import logging


def configure_logging(settings: Settings) -> None:
    """Configure logging for the application.

    Args:
        settings: Application settings
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, settings.log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(settings.LOGGING.FORMAT)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler if log file is specified
    if hasattr(settings.LOGGING, "LOG_FILE") and settings.LOGGING.LOG_FILE:
        file_handler = logging.FileHandler(settings.LOGGING.LOG_FILE)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

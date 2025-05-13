"""
Core logging module.

Provides centralized logging configuration and utilities for the application.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import cast

from core.utils.config import DEFAULT_ENCODING, LOG_DIR, LOGGING_CONFIG


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure a logger with standardized formatting.

    Args:
        name: Name of the logger
        level: Logging level (default: INFO)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Only configure if no handlers exist
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(
            logging.Formatter(
                fmt=cast(str, LOGGING_CONFIG["format"]),
                datefmt=cast(str, LOGGING_CONFIG["datefmt"]),
            )
        )
        logger.addHandler(console_handler)

        # File handler
        if not LOG_DIR.exists():
            os.makedirs(LOG_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"log-{timestamp}-{name}.txt"

        file_handler = logging.FileHandler(
            log_file,
            encoding=DEFAULT_ENCODING,
        )
        file_handler.setFormatter(
            logging.Formatter(
                fmt=cast(str, LOGGING_CONFIG["format"]),
                datefmt=cast(str, LOGGING_CONFIG["datefmt"]),
            )
        )
        logger.addHandler(file_handler)

        # Silence noisy loggers
        for noisy_logger in LOGGING_CONFIG["noisy_loggers"]:
            logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    return setup_logger(name)


# Convenience functions for common logging operations
def log_info(message: str, logger_name: str = "root") -> None:
    """Log an INFO level message."""
    logging.getLogger(logger_name).info(message)


def log_warning(message: str, logger_name: str = "root") -> None:
    """Log a WARNING level message."""
    logging.getLogger(logger_name).warning(message)


def log_error(message: str, logger_name: str = "root") -> None:
    """Log an ERROR level message."""
    logging.getLogger(logger_name).error(message) 
"""
Core logging module.

Provides centralized logging configuration and utilities for the application.
"""

from core.config import config
from datetime import datetime
from typing import Optional, Dict, Any
import os

import logging
import logging.handlers


def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with file and console handlers.

    Args:
        name: The name of the logger

    Returns:
        A configured logger instance
    """
    # Create log directories if they don't exist
    os.makedirs(config.PATHS.LOG_DIR, exist_ok=True)
    os.makedirs(config.PATHS.TEST_RESULTS_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create formatters
    file_formatter = logging.Formatter(
        config.LOGGING.FORMAT,
        datefmt=config.LOGGING.DATE_FORMAT
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Create and configure file handler with rotation
    log_file = config.PATHS.LOG_DIR / f"{name}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        str(log_file),
        maxBytes=config.CACHE.MAX_SIZE,
        backupCount=config.CACHE.TTL
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        name: The name of the logger

    Returns:
        A configured logger instance
    """
    return setup_logger(name)


def log_operation(
    operation: str,
    details: Optional[Dict[str, Any]] = None,
    logger_name: str = "operations"
) -> None:
    """Log an operation with details.

    Args:
        operation: The operation being performed
        details: Additional details about the operation
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)
    message = f"Operation: {operation}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)


def log_error(
    operation: str,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
    logger_name: str = "errors"
) -> None:
    """Log an error with context.

    Args:
        operation: The operation that failed
        error: The exception that occurred
        context: Additional context about the error
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)
    message = f"Error in {operation}: {str(error)}"
    if context:
        message += f" - Context: {context}"
    logger.error(message)


def log_performance(
    operation: str,
    duration: float,
    metrics: Optional[Dict[str, Any]] = None,
    logger_name: str = "performance"
) -> None:
    """Log performance metrics.

    Args:
        operation: The operation being measured
        duration: The duration of the operation in seconds
        metrics: Additional performance metrics
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)
    message = f"Performance: {operation} - Duration: {duration:.2f}s"
    if metrics:
        message += f" - Metrics: {metrics}"
    logger.info(message)


def log_test_result(
    test_name: str,
    status: str,
    duration: float,
    details: Optional[str] = None
) -> None:
    """Log a test result.

    Args:
        test_name: The name of the test
        status: The test status (PASSED / FAILED)
        duration: The test duration in seconds
        details: Additional test details
    """
    logger = get_logger("test")
    message = f"Test: {test_name} - Status: {status} - Duration: {duration:.2f}s"
    if details:
        message += f" - Details: {details}"
    logger.info(message)

    # Also write to test results file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = config.PATHS.TEST_RESULTS_DIR / f"test_run_{timestamp}.log"
    with open(result_file, "a") as f:
        f.write(f"{message}\n")


# Convenience functions for common logging operations


def log_info(message: str, logger_name: str = "root") -> None:
    """Log an INFO level message.

    Args:
        message: The message to log
        logger_name: Name of the logger to use
    """
    logging.getLogger(logger_name).info(message)


def log_warning(message: str, logger_name: str = "root") -> None:
    """Log a WARNING level message.

    Args:
        message: The message to log
        logger_name: Name of the logger to use
    """
    logging.getLogger(logger_name).warning(message)


def log_error_message(message: str, logger_name: str = "root") -> None:
    """Log an ERROR level message.

    Args:
        message: The message to log
        logger_name: Name of the logger to use
    """
    logging.getLogger(logger_name).error(message)

"""
Logging module.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import json
import sys

import logging

class JSONFormatter(logging.Formatter):
    """JSON formatter for logs."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON.

        Args:
            record: Log record to format

        Returns:
            str: Formatted log record
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(), 
            "level": record.levelname, 
            "message": record.getMessage(), 
            "module": record.module, 
            "function": record.funcName, 
            "line": record.lineno
        }

        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__, 
                "message": str(record.exc_info[1]), 
                "traceback": self.formatException(record.exc_info)
            }

        return json.dumps(log_data)

def setup_logger(
    name: str, 
    level: int = logging.INFO, 
    log_file: Optional[Path] = None, 
    json_format: bool = True
) -> logging.Logger:
    """Set up a logger.

    Args:
        name: Logger name
        level: Logging level
        log_file: Optional log file path
        json_format: Whether to use JSON format

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Create loggers
generation_logger = setup_logger("recipe_generation")
extraction_logger = setup_logger("recipe_extraction")
metrics_logger = setup_logger("metrics")

def log_metric(
    logger: logging.Logger, 
    metric_name: str, 
    value: float, 
    labels: Optional[Dict[str, str]] = None
) -> None:
    """Log a metric.

    Args:
        logger: Logger to use
        metric_name: Metric name
        value: Metric value
        labels: Optional labels
    """
    extra = {
        "metric_name": metric_name, 
        "value": value
    }

    if labels:
        extra["labels"] = labels

    logger.info(f"Metric: {metric_name}", extra = extra)

def log_error(
    logger: logging.Logger, 
    error: Exception, 
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log an error.

    Args:
        logger: Logger to use
        error: Error to log
        context: Optional context
    """
    extra = {
        "error_type": error.__class__.__name__, 
        "error_message": str(error)
    }

    if context:
        extra["context"] = context

    logger.error(f"Error: {error}", exc_info = True, extra = extra)

def log_warning(
    logger: logging.Logger, 
    message: str, 
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log a warning.

    Args:
        logger: Logger to use
        message: Warning message
        context: Optional context
    """
    extra = {}
    if context:
        extra["context"] = context

    logger.warning(message, extra = extra)

def log_info(
    logger: logging.Logger, 
    message: str, 
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log an info message.

    Args:
        logger: Logger to use
        message: Info message
        context: Optional context
    """
    extra = {}
    if context:
        extra["context"] = context

    logger.info(message, extra = extra)

def log_debug(
    logger: logging.Logger, 
    message: str, 
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log a debug message.

    Args:
        logger: Logger to use
        message: Debug message
        context: Optional context
    """
    extra = {}
    if context:
        extra["context"] = context

    logger.debug(message, extra = extra)

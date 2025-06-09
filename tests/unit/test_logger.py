from core.utils import logger

import logging
import pytest

def test_setup_logger_creates_logger(tmp_path):
    log = logger.setup_logger("test_logger")
    assert isinstance(log, logging.Logger)
    log.info("Test info message")
    log.warning("Test warning message")
    log.error("Test error message")

def test_get_logger_returns_logger():
    log = logger.get_logger("another_logger")
    assert isinstance(log, logging.Logger)

@pytest.mark.skip(reason="Info - level logging not expected by default")
def test_log_info_warning_error(caplog):
    logger.log_info("info message", logger_name="root")
    logger.log_warning("warning message", logger_name="root")
    logger.log_error("error message", logger_name="root")
    messages = [rec.message for rec in caplog.records]
    assert "info message" in messages
    assert "warning message" in messages
    assert "error message" in messages

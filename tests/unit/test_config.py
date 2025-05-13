import pytest
from pathlib import Path
from core.utils import config

def test_constants():
    assert config.PROJECT_NAME == "Plan Mensual Comidas"
    assert config.VERSION
    assert config.DEFAULT_ENCODING == "utf-8"
    assert ".txt" in config.TEXT_EXTENSIONS
    assert ".pdf" in config.PDF_EXTENSIONS
    assert ".jpg" in config.IMAGE_EXTENSIONS

def test_is_supported_extension():
    assert config.is_supported_extension(Path("file.txt"))
    assert config.is_supported_extension(Path("file.pdf"))
    assert config.is_supported_extension(Path("file.jpg"))
    assert not config.is_supported_extension(Path("file.exe"))

def test_get_file_type():
    assert config.get_file_type(Path("file.txt")) == "text"
    assert config.get_file_type(Path("file.pdf")) == "pdf"
    assert config.get_file_type(Path("file.png")) == "image"
    assert config.get_file_type(Path("file.exe")) == "unknown" 
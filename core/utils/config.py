"""
Core configuration module.

Defines constants, paths, and project-wide configurations.
"""

import os
from pathlib import Path

# Project information
PROJECT_NAME = "Plan Mensual Comidas"
VERSION = "1.5.0"

# Main directories
WORK_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
RECIPES_DIR = WORK_DIR / "recetas"
UNPROCESSED_DIR = RECIPES_DIR / "sin_procesar"
JSON_RECIPES_DIR = RECIPES_DIR / "procesadas" / "Recetas JSON"
ORIGINAL_RECIPES_DIR = RECIPES_DIR / "procesadas" / "Recetas Originales"
MD_RECIPES_DIR = RECIPES_DIR / "procesadas" / "Recetas MD"
LOG_DIR = WORK_DIR / ".log"

# Default encoding
DEFAULT_ENCODING = "utf-8"

# Supported file extensions
TEXT_EXTENSIONS = {".txt", ".md", ".rst"}
PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}

# Logging configuration
LOGGING_CONFIG = {
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
    "noisy_loggers": [
        "PIL.PngImagePlugin",
        "PIL.TiffImagePlugin",
        "pdfminer.pdfinterp",
        "pdfminer.pdfdocument",
        "pdfminer.pdfpage",
        "pdfminer.converter",
        "pdfminer.cmapdb",
        "pdfminer.layout",
    ],
}


def is_supported_extension(path: Path) -> bool:
    """
    Check if the file extension is supported.

    Args:
        path: Path to the file

    Returns:
        bool: True if the extension is supported
    """
    ext = path.suffix.lower()
    return ext in TEXT_EXTENSIONS | PDF_EXTENSIONS | IMAGE_EXTENSIONS


def get_file_type(path: Path) -> str:
    """
    Determine the file type based on its extension.

    Args:
        path: Path to the file

    Returns:
        str: File type ('text', 'pdf', 'image', or 'unknown')
    """
    ext = path.suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in PDF_EXTENSIONS:
        return "pdf"
    if ext in IMAGE_EXTENSIONS:
        return "image"
    return "unknown" 
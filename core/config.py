"""
Módulo de configuración global.

Define constantes, rutas y configuraciones del proyecto.
"""

import os
from pathlib import Path

# Información del proyecto
NOMBRE_PROYECTO = "Plan Mensual Comidas"
VERSION = "1.5.0"

# Directorios principales
DIR_TRABAJO = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR_RECETAS = DIR_TRABAJO / "recetas"
DIR_SIN_PROCESAR = DIR_RECETAS / "sin_procesar"
DIR_RECETAS_JSON = DIR_RECETAS / "procesadas" / "Recetas JSON"
DIR_RECETAS_ORIGINALES = DIR_RECETAS / "procesadas" / "Recetas Originales"
DIR_RECETAS_MD = DIR_RECETAS / "procesadas" / "Recetas MD"
LOG_DIR = DIR_TRABAJO / ".log"

# Codificación por defecto
ENCODING_DEFAULT = "utf-8"

# Extensiones soportadas
EXTENSIONES_TEXTO = {".txt", ".md", ".rst"}
EXTENSIONES_PDF = {".pdf"}
EXTENSIONES_IMAGEN = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp"}

# Configuración de logging
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


def es_extension_soportada(path: Path) -> bool:
    """
    Verifica si la extensión del archivo es soportada.

    Args:
        path: Ruta al archivo

    Returns:
        bool: True si la extensión es soportada
    """
    ext = path.suffix.lower()
    return ext in EXTENSIONES_TEXTO | EXTENSIONES_PDF | EXTENSIONES_IMAGEN


def obtener_tipo_archivo(path: Path) -> str:
    """
    Determina el tipo de archivo basado en su extensión.

    Args:
        path: Ruta al archivo

    Returns:
        str: Tipo de archivo ('texto', 'pdf', 'imagen' o 'desconocido')
    """
    ext = path.suffix.lower()
    if ext in EXTENSIONES_TEXTO:
        return "texto"
    if ext in EXTENSIONES_PDF:
        return "pdf"
    if ext in EXTENSIONES_IMAGEN:
        return "imagen"
    return "desconocido"

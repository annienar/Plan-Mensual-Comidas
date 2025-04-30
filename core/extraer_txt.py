"""
Módulo para extraer texto de archivos de texto plano.

Maneja la lectura de archivos .txt con diferentes codificaciones.
"""

from pathlib import Path

from core.config import ENCODING_DEFAULT
from core.logger import configurar_logger, log_error

logger = configurar_logger("extraer_txt")


def extraer_texto_desde_txt(ruta: Path) -> str:
    """
    Extrae texto de un archivo .txt.

    Args:
        ruta: Ruta al archivo de texto

    Returns:
        str: Contenido del archivo de texto
    """
    try:
        return ruta.read_text(encoding=ENCODING_DEFAULT)
    except UnicodeError:
        # Intenta con otras codificaciones comunes
        for encoding in ["utf-8", "latin1", "cp1252"]:
            try:
                return ruta.read_text(encoding=encoding)
            except UnicodeError:
                continue
        log_error(f"No se pudo determinar la codificación de {ruta}")
        return ""
    except Exception as e:
        log_error(f"Error al leer {ruta}: {e}")
        return ""

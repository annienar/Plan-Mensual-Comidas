"""
Módulo para extraer texto de archivos PDF.

Utiliza pdfplumber para extraer texto de PDFs.
"""

from pathlib import Path

import pdfplumber

from core.logger import configurar_logger, log_error

logger = configurar_logger("extraer_pdf")


def extraer_texto_desde_pdf(ruta: Path) -> str:
    """
    Extrae el texto de un archivo PDF.

    Args:
        ruta: Ruta al archivo PDF

    Returns:
        str: Texto extraído del PDF
    """
    try:
        with pdfplumber.open(ruta) as pdf:
            return "\n\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        log_error(f"Error al extraer texto del PDF {ruta}: {e}")
        return ""

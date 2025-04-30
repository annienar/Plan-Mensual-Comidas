"""
Módulo para extraer texto de imágenes mediante OCR.

Utiliza Tesseract OCR a través de pytesseract.
"""

from pathlib import Path
from typing import List

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from core.logger import configurar_logger, log_error, log_info

logger = configurar_logger("extraer_ocr")


def _procesar_imagen(imagen: Image.Image) -> str:
    """
    Procesa una imagen con OCR para extraer texto.

    Args:
        imagen: Imagen a procesar

    Returns:
        str: Texto extraído de la imagen
    """
    try:
        texto: str = pytesseract.image_to_string(imagen, lang="spa")
        return texto if texto else ""
    except Exception as e:
        log_error(f"Error en OCR: {e}")
        return ""


def extraer_texto_desde_imagen(ruta: Path) -> str:
    """
    Extrae texto de un archivo de imagen o PDF mediante OCR.

    Args:
        ruta: Ruta al archivo de imagen o PDF

    Returns:
        str: Texto extraído mediante OCR
    """
    try:
        if ruta.suffix.lower() == ".pdf":
            imagenes = convert_from_path(ruta)
        else:
            imagenes = [Image.open(ruta)]

        textos: List[str] = []
        for imagen in imagenes:
            texto = _procesar_imagen(imagen)
            if texto.strip():
                textos.append(texto.strip())

        return "\n\n".join(textos)

    except Exception as e:
        log_error(f"Error al procesar {ruta}: {e}")
        return ""


def extraer_texto_desde_pdf_ocr(path_pdf: str) -> str:
    """
    Extrae texto de un archivo PDF mediante OCR.

    Args:
        path_pdf: Ruta al archivo PDF a procesar

    Returns:
        str: Texto extraído del PDF mediante OCR
    """
    texto_extraido = ""
    try:
        paginas = convert_from_path(path_pdf)
        for _, pagina in enumerate(paginas):
            texto = pytesseract.image_to_string(pagina, lang="spa")
            if texto:
                texto_extraido += texto + "\n"
        log_info(f"📄 Texto extraído mediante OCR de {path_pdf}")
    except Exception as e:
        log_error(f"❌ Error al procesar PDF mediante OCR {path_pdf}: {e}")
    return texto_extraido.strip()


def extraer_texto_desde_ocr(path_archivo: str) -> str:
    """Alias simple para compatibilidad con procesar_recetas."""
    return extraer_texto_desde_pdf_ocr(path_archivo)

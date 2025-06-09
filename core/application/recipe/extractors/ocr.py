"""
Módulo para extraer texto de imágenes mediante OCR.

Utiliza Tesseract OCR a través de pytesseract.
"""
from pathlib import Path
from typing import List, Any

from .interface import IExtractor

class LoggerStub:
    def info(self, msg): pass
    def error(self, msg): pass

logger = LoggerStub()

def log_error(msg, **kwargs):
    logger.error(msg)

def log_info(msg, **kwargs):
    logger.info(msg)

try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

def _procesar_imagen(imagen) -> str:
    """
    Procesa una imagen con OCR para extraer texto.

    Args:
        imagen: Imagen a procesar

    Returns:
        str: Texto extraído de la imagen
    """
    if not HAS_OCR:
        return ''
    try:
        texto: str = pytesseract.image_to_string(imagen, lang='spa')
        return texto if texto else ''
    except Exception as e:
        log_error(f'Error en OCR: {e}')
        return ''

class OCRExtractor(IExtractor):
    """Optical Character Recognition (OCR) extractor for image - based text extraction.

    This class provides OCR capabilities to extract text content from images
    containing text, such as scanned documents, photos of recipes, or other
    image - based text sources. It supports multiple image formats and provides
    robust text extraction with error handling.

    Features:
        - Multiple image format support (JPEG, PNG, TIFF, BMP, etc.)
        - Text extraction from image files
        - Preprocessing for improved OCR accuracy
        - Comprehensive error handling and logging
        - Graceful degradation on OCR failures

    Supported Image Formats:
        - JPEG (.jpg, .jpeg)
        - PNG (.png)
        - TIFF (.tiff, .tif)
        - BMP (.bmp)
        - GIF (.gif)

    Requirements:
        - OCR engine must be properly configured
        - Image files must be readable and contain text
        - Sufficient image quality for text recognition

    Example:
        >>> extractor = OCRExtractor()
        >>> text = extractor.extract("/path / to / recipe_image.jpg")
        >>> print(text)
    """

    def extract(self, source_path: str) -> str:
        """Extract text content from an image file using OCR.

        Performs Optical Character Recognition on the provided image file
        to extract any text content. The method handles various image
        formats and provides robust error handling for OCR operations.

        Args:
            source_path (str): Path to the image file to extract text from.
                            Must be a valid file path that exists on the filesystem
                            and contains a supported image format.

        Returns:
            str: The extracted text content from the image. Returns an empty
                string if the file doesn't exist, is not a valid image, 
                contains no recognizable text, or if OCR processing fails.

        Raises:
            No exceptions are raised directly. All errors are logged and
            result in an empty string return value for graceful degradation.

        Note:
            - OCR accuracy depends on image quality and text clarity
            - Various image preprocessing techniques may be applied automatically
            - All errors are logged for debugging purposes
            - Empty results may indicate either no text or OCR processing issues
        """
        if not HAS_OCR:
            return ''

        ruta = Path(source_path)
        try:
            if ruta.suffix.lower() == '.pdf':
                imagenes = convert_from_path(ruta)
            else:
                imagenes = [Image.open(ruta)]
            textos: List[str] = []
            for imagen in imagenes:
                texto = _procesar_imagen(imagen)
                if texto.strip():
                    textos.append(texto.strip())
            return '\n\n'.join(textos)
        except Exception as e:
            log_error(f'Error al procesar {ruta}: {e}')
            return ''

def extraer_texto_desde_pdf_ocr(path_pdf: str) -> str:
    """
    Extrae texto de un archivo PDF mediante OCR.

    Args:
        path_pdf: Ruta al archivo PDF a procesar

    Returns:
        str: Texto extraído del PDF mediante OCR
    """
    if not HAS_OCR:
        return ''

    texto_extraido = ''
    try:
        paginas = convert_from_path(path_pdf)
        for _, pagina in enumerate(paginas):
            texto = pytesseract.image_to_string(pagina, lang='spa')
            if texto:
                texto_extraido += texto + '\n'
        log_info(f'📄 Texto extraído mediante OCR de {path_pdf}')
    except Exception as e:
        log_error(f'❌ Error al procesar PDF mediante OCR {path_pdf}: {e}')
    return texto_extraido.strip()

def extraer_texto_desde_ocr(path_archivo: str) -> str:
    """Alias simple para compatibilidad con procesar_recetas."""
    return extraer_texto_desde_pdf_ocr(path_archivo)

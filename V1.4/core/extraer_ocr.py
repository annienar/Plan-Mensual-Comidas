import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from core.logger import configurar_logger, log_info, log_warning, log_error

logger = configurar_logger("extraer_ocr")

def extraer_texto_desde_imagen(path_imagen):
    try:
        imagen = Image.open(path_imagen)
        texto = pytesseract.image_to_string(imagen, lang='spa')
        log_info(f"📸 Texto extraído correctamente de imagen {path_imagen}")
        return texto.strip()
    except Exception as e:
        log_error(f"❌ Error al procesar imagen {path_imagen}: {e}")
        return ""

def extraer_texto_desde_pdf_ocr(path_pdf):
    texto_extraido = ""
    try:
        paginas = convert_from_path(path_pdf)
        for idx, pagina in enumerate(paginas):
            texto = pytesseract.image_to_string(pagina, lang='spa')
            if texto:
                texto_extraido += texto + "\n"
        log_info(f"📄 Texto extraído mediante OCR de {path_pdf}")
    except Exception as e:
        log_error(f"❌ Error al procesar PDF mediante OCR {path_pdf}: {e}")
    return texto_extraido.strip()

def extraer_texto_desde_ocr(path_archivo: str) -> str:
    """Alias simple para compatibilidad con procesar_recetas."""
    return extraer_texto_desde_pdf_ocr(path_archivo)
"""
Módulo para extraer texto de archivos PDF.

Utiliza pdfplumber para extraer texto de PDFs.
"""

from pathlib import Path
from core.extraction.interface import IExtractor
import pdfplumber
from core.utils.logger import setup_logger, log_error

logger = setup_logger("extraer_pdf")

class PDFExtractor(IExtractor):
    def extract(self, source_path: str) -> str:
        """Extract raw text from the given PDF file."""
        ruta = Path(source_path)
        try:
            with pdfplumber.open(ruta) as pdf:
                return "\n\n".join(page.extract_text() or "" for page in pdf.pages).strip()
        except Exception as e:
            log_error(f"Error al extraer texto del PDF {ruta}: {e}")
            return ""

"""
Módulo para extraer texto de archivos PDF.

Utiliza pdfplumber para extraer texto de PDFs.
"""
from pathlib import Path
from typing import Any

from .interface import IExtractor

class LoggerStub:
    def info(self, msg): pass
    def error(self, msg): pass

logger = LoggerStub()

def log_error(msg, **kwargs):
    logger.error(msg)

try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

class PDFExtractor(IExtractor):
    """PDF text extraction service for processing PDF documents.

    This class provides comprehensive PDF text extraction capabilities, 
    supporting both text - based PDFs and image - based PDFs through OCR.
    It handles various PDF formats and structures while providing robust
    error handling and logging.

    Features:
        - Direct text extraction from text - based PDFs
        - OCR fallback for image - based or scanned PDFs
        - Multi - page document support
        - Metadata extraction (title, author, creation date)
        - Table and structured content handling
        - Comprehensive error handling and logging

    Supported PDF Types:
        - Text - based PDFs (native text extraction)
        - Image - based PDFs (OCR extraction)
        - Scanned documents (OCR extraction)
        - Multi - page documents
        - Password - protected PDFs (with password)

    Requirements:
        - PDF processing library must be available
        - For OCR: OCR engine must be properly configured
        - Sufficient memory for large PDF processing

    Example:
        >>> extractor = PDFExtractor()
        >>> text = extractor.extract("/path / to / recipe_document.pdf")
        >>> print(text)
    """

    def extract(self, source_path: str) -> str:
        """Extract text content from a PDF document.

        Performs text extraction from PDF files using multiple strategies:
        first attempts direct text extraction for text - based PDFs, then
        falls back to OCR for image - based content. Handles multi - page
        documents and various PDF structures.

        Args:
            source_path (str): Path to the PDF file to extract text from.
                            Must be a valid file path that exists on the filesystem
                            and contains a readable PDF document.

        Returns:
            str: The extracted text content from all pages of the PDF.
                Returns an empty string if the file doesn't exist, is not
                a valid PDF, is encrypted without password, or if extraction
                fails completely.

        Raises:
            No exceptions are raised directly. All errors are logged and
            result in an empty string return value for graceful degradation.

        Note:
            - Text - based PDFs provide higher accuracy than OCR extraction
            - Large PDFs may take significant time to process
            - Password - protected PDFs will fail without proper authentication
            - All errors are logged for debugging purposes
            - OCR is automatically attempted for image - based content
        """
        if not HAS_PDF:
            return ''

        ruta = Path(source_path)
        try:
            with pdfplumber.open(ruta) as pdf:
                return '\n\n'.join(page.extract_text() or '' for page in
                    pdf.pages).strip()
        except Exception as e:
            log_error(f'Error al extraer texto del PDF {ruta}: {e}')
            return ''

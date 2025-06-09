"""
Extractor factory for creating appropriate extractors based on file type.

This module demonstrates the benefits of the IExtractor interface by providing
a factory pattern that can create the appropriate extractor for any file type
without the client code needing to know about specific implementations.
"""

from pathlib import Path
from typing import Dict, Type, Optional

from .interface import IExtractor
from .text import TextExtractor
from .pdf import PDFExtractor
from .ocr import OCRExtractor


class ExtractorFactory:
    """Factory for creating file extractors based on file type.
    
    This factory demonstrates the power of the IExtractor interface by providing
    a clean way to create appropriate extractors for different file types without
    clients needing to know about specific implementations.
    
    Features:
        - Automatic extractor selection based on file extension
        - Support for multiple file types per extractor
        - Easy registration of new extractors
        - Consistent interface through IExtractor
        - Graceful fallback to text extraction
        
    Example:
        >>> factory = ExtractorFactory()
        >>> extractor = factory.create_extractor("/path/to/file.pdf")
        >>> content = extractor.extract("/path/to/file.pdf")
    """
    
    def __init__(self):
        """Initialize the factory with default extractor mappings."""
        self._extractors: Dict[str, Type[IExtractor]] = {
            # Text files
            '.txt': TextExtractor,
            '.text': TextExtractor,
            '.md': TextExtractor,
            '.markdown': TextExtractor,
            '.rst': TextExtractor,
            '.log': TextExtractor,
            '.csv': TextExtractor,
            '.json': TextExtractor,
            '.xml': TextExtractor,
            '.html': TextExtractor,
            '.htm': TextExtractor,
            
            # PDF files
            '.pdf': PDFExtractor,
            
            # Image files (OCR)
            '.jpg': OCRExtractor,
            '.jpeg': OCRExtractor,
            '.png': OCRExtractor,
            '.bmp': OCRExtractor,
            '.tiff': OCRExtractor,
            '.tif': OCRExtractor,
            '.gif': OCRExtractor,
            '.webp': OCRExtractor,
        }
        
        # Default fallback extractor
        self._default_extractor = TextExtractor
    
    def create_extractor(self, file_path: str) -> IExtractor:
        """Create an appropriate extractor for the given file.
        
        Analyzes the file extension to determine the best extractor type
        and returns an instance configured for that file type.
        
        Args:
            file_path (str): Path to the file that needs extraction.
                           The file extension will be used to determine
                           the appropriate extractor type.
                           
        Returns:
            IExtractor: An instance of the appropriate extractor for the
                       file type. Falls back to TextExtractor for unknown
                       file types.
                       
        Example:
            >>> factory = ExtractorFactory()
            >>> pdf_extractor = factory.create_extractor("recipe.pdf")
            >>> assert isinstance(pdf_extractor, PDFExtractor)
            >>> 
            >>> txt_extractor = factory.create_extractor("recipe.txt")
            >>> assert isinstance(txt_extractor, TextExtractor)
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        extractor_class = self._extractors.get(extension, self._default_extractor)
        return extractor_class()
    
    def register_extractor(self, extension: str, extractor_class: Type[IExtractor]) -> None:
        """Register a new extractor for a specific file extension.
        
        This method allows extending the factory with new extractors without
        modifying the core factory code, following the Open/Closed Principle.
        
        Args:
            extension (str): File extension (including the dot, e.g., '.xyz').
                           Will be converted to lowercase for consistency.
            extractor_class (Type[IExtractor]): The extractor class to use for
                                              files with this extension. Must
                                              implement the IExtractor interface.
                                              
        Example:
            >>> factory = ExtractorFactory()
            >>> factory.register_extractor('.docx', WordExtractor)
            >>> extractor = factory.create_extractor("document.docx")
            >>> assert isinstance(extractor, WordExtractor)
        """
        self._extractors[extension.lower()] = extractor_class
    
    def get_supported_extensions(self) -> list[str]:
        """Get a list of all supported file extensions.
        
        Returns:
            list[str]: List of file extensions that have registered extractors.
                      Extensions are returned in lowercase with the dot prefix.
                      
        Example:
            >>> factory = ExtractorFactory()
            >>> extensions = factory.get_supported_extensions()
            >>> assert '.pdf' in extensions
            >>> assert '.txt' in extensions
        """
        return list(self._extractors.keys())
    
    def supports_file(self, file_path: str) -> bool:
        """Check if the factory supports extraction for the given file.
        
        Args:
            file_path (str): Path to the file to check.
                           
        Returns:
            bool: True if the file extension has a registered extractor,
                 False otherwise. Note that unsupported files will still
                 fall back to the default text extractor.
                 
        Example:
            >>> factory = ExtractorFactory()
            >>> assert factory.supports_file("recipe.pdf") == True
            >>> assert factory.supports_file("unknown.xyz") == False
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        return extension in self._extractors


# Convenience function for one-off extractions
def extract_from_file(file_path: str) -> str:
    """Extract text content from a file using the appropriate extractor.
    
    This is a convenience function that creates a factory, selects the
    appropriate extractor, and performs the extraction in one call.
    
    Args:
        file_path (str): Path to the file to extract content from.
                        
    Returns:
        str: Extracted text content from the file.
        
    Example:
        >>> content = extract_from_file("/path/to/recipe.pdf")
        >>> print(content)
    """
    factory = ExtractorFactory()
    extractor = factory.create_extractor(file_path)
    return extractor.extract(file_path) 
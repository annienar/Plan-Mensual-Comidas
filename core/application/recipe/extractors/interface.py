"""
Application layer extractor interface.

This module defines the interface contract that all application layer
extractors must implement. This provides consistency, testability,
and loose coupling for file extraction services.
"""

from abc import ABC, abstractmethod


class IExtractor(ABC):
    """Generic extractor interface for application file extraction services.
    
    This interface defines the contract that all application layer extractors
    must implement. It provides a consistent API for extracting text content
    from various file types while maintaining clean architecture principles.
    
    Features:
        - Consistent interface across all file extraction services
        - Support for dependency injection and polymorphism
        - Easy testing and mocking capabilities
        - Extensible design for new file types
        
    Implementation Requirements:
        - All extractors must implement the extract() method
        - Extract method must accept a file path and return text content
        - Error handling should be graceful with empty string returns
        - All implementations should include comprehensive logging
        
    Example:
        >>> extractor: IExtractor = TextExtractor()
        >>> content = extractor.extract("/path/to/file.txt")
        >>> print(content)
    """
    
    @abstractmethod
    def extract(self, source_path: str) -> str:
        """Extract text content from a file.
        
        This method defines the core contract for all file extraction services.
        Implementations should handle various file formats and provide robust
        error handling while maintaining consistent behavior across extractors.
        
        Args:
            source_path (str): Path to the file to extract content from.
                            Must be a valid file path that exists on the filesystem.
                            
        Returns:
            str: The extracted text content from the file. Should return an
                empty string if extraction fails, file doesn't exist, or 
                no content can be extracted.
                
        Raises:
            No exceptions should be raised directly. All errors should be
            handled gracefully and logged appropriately, returning an empty
            string for failed extractions.
            
        Note:
            - Implementations should validate file existence
            - All errors should be logged for debugging
            - Empty results should be handled gracefully
            - File encoding issues should be handled automatically
        """
        pass 
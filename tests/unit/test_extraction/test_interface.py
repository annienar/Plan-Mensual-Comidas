"""
Tests for the IExtractor interface and ExtractorFactory.

These tests demonstrate the benefits of the interface-based architecture
and ensure that all extractors follow the same contract.
"""

import pytest
from unittest.mock import patch, MagicMock
import tempfile
from pathlib import Path

from core.application.recipe.extractors.interface import IExtractor
from core.application.recipe.extractors.factory import ExtractorFactory, extract_from_file
from core.application.recipe.extractors.text import TextExtractor
from core.application.recipe.extractors.pdf import PDFExtractor
from core.application.recipe.extractors.ocr import OCRExtractor


class TestIExtractorInterface:
    """Test the IExtractor interface compliance."""
    
    def test_text_extractor_implements_interface(self):
        """Test that TextExtractor implements IExtractor interface."""
        extractor = TextExtractor()
        assert isinstance(extractor, IExtractor)
        assert hasattr(extractor, 'extract')
        assert callable(extractor.extract)
    
    def test_pdf_extractor_implements_interface(self):
        """Test that PDFExtractor implements IExtractor interface."""
        extractor = PDFExtractor()
        assert isinstance(extractor, IExtractor)
        assert hasattr(extractor, 'extract')
        assert callable(extractor.extract)
    
    def test_ocr_extractor_implements_interface(self):
        """Test that OCRExtractor implements IExtractor interface."""
        extractor = OCRExtractor()
        assert isinstance(extractor, IExtractor)
        assert hasattr(extractor, 'extract')
        assert callable(extractor.extract)
    
    def test_interface_polymorphism(self):
        """Test that different extractors can be used polymorphically."""
        extractors = [
            TextExtractor(),
            PDFExtractor(),
            OCRExtractor()
        ]
        
        # All should be IExtractor instances
        for extractor in extractors:
            assert isinstance(extractor, IExtractor)
        
        # All should have the same interface
        def process_with_extractor(extractor: IExtractor, path: str) -> str:
            return extractor.extract(path)
        
        # This should work with any extractor (polymorphism)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            f.flush()
            
            try:
                # Test polymorphic behavior
                for extractor in extractors:
                    # All should accept the same method signature
                    result = process_with_extractor(extractor, f.name)
                    # Result should be a string (may be empty for some extractors)
                    assert isinstance(result, str)
            finally:
                Path(f.name).unlink()


class TestExtractorFactory:
    """Test the ExtractorFactory implementation."""
    
    def test_factory_creation(self):
        """Test factory instance creation."""
        factory = ExtractorFactory()
        assert factory is not None
        assert hasattr(factory, 'create_extractor')
    
    def test_text_file_extractor_selection(self):
        """Test that factory selects TextExtractor for text files."""
        factory = ExtractorFactory()
        
        text_extensions = ['.txt', '.md', '.json', '.csv']
        for ext in text_extensions:
            extractor = factory.create_extractor(f"test{ext}")
            assert isinstance(extractor, TextExtractor)
            assert isinstance(extractor, IExtractor)
    
    def test_pdf_file_extractor_selection(self):
        """Test that factory selects PDFExtractor for PDF files."""
        factory = ExtractorFactory()
        
        extractor = factory.create_extractor("test.pdf")
        assert isinstance(extractor, PDFExtractor)
        assert isinstance(extractor, IExtractor)
    
    def test_image_file_extractor_selection(self):
        """Test that factory selects OCRExtractor for image files."""
        factory = ExtractorFactory()
        
        image_extensions = ['.jpg', '.png', '.bmp', '.tiff']
        for ext in image_extensions:
            extractor = factory.create_extractor(f"test{ext}")
            assert isinstance(extractor, OCRExtractor)
            assert isinstance(extractor, IExtractor)
    
    def test_unknown_extension_fallback(self):
        """Test that factory falls back to TextExtractor for unknown extensions."""
        factory = ExtractorFactory()
        
        extractor = factory.create_extractor("test.unknown")
        assert isinstance(extractor, TextExtractor)
        assert isinstance(extractor, IExtractor)
    
    def test_case_insensitive_extension_matching(self):
        """Test that extension matching is case insensitive."""
        factory = ExtractorFactory()
        
        # Test uppercase extensions
        extractor1 = factory.create_extractor("test.PDF")
        extractor2 = factory.create_extractor("test.TXT")
        extractor3 = factory.create_extractor("test.JPG")
        
        assert isinstance(extractor1, PDFExtractor)
        assert isinstance(extractor2, TextExtractor)
        assert isinstance(extractor3, OCRExtractor)
    
    def test_supported_extensions(self):
        """Test getting list of supported extensions."""
        factory = ExtractorFactory()
        extensions = factory.get_supported_extensions()
        
        assert isinstance(extensions, list)
        assert '.txt' in extensions
        assert '.pdf' in extensions
        assert '.jpg' in extensions
        assert len(extensions) > 0
    
    def test_supports_file_method(self):
        """Test the supports_file method."""
        factory = ExtractorFactory()
        
        assert factory.supports_file("test.txt") == True
        assert factory.supports_file("test.pdf") == True
        assert factory.supports_file("test.jpg") == True
        assert factory.supports_file("test.unknown") == False
    
    def test_register_new_extractor(self):
        """Test registering a new extractor type."""
        factory = ExtractorFactory()
        
        # Register TextExtractor for .custom extension
        factory.register_extractor('.custom', TextExtractor)
        
        # Test that it's now supported
        assert factory.supports_file("test.custom") == True
        extractor = factory.create_extractor("test.custom")
        assert isinstance(extractor, TextExtractor)
    
    def test_factory_provides_consistent_interface(self):
        """Test that all factory-created extractors have consistent interface."""
        factory = ExtractorFactory()
        
        test_files = [
            "recipe.txt",
            "recipe.pdf", 
            "recipe.jpg",
            "recipe.unknown"
        ]
        
        for file_path in test_files:
            extractor = factory.create_extractor(file_path)
            assert isinstance(extractor, IExtractor)
            assert hasattr(extractor, 'extract')
            assert callable(extractor.extract)


class TestConvenienceFunction:
    """Test the convenience extract_from_file function."""
    
    def test_extract_from_file_function_exists(self):
        """Test that the convenience function exists and is callable."""
        assert callable(extract_from_file)
    
    @patch('core.application.recipe.extractors.text.TextExtractor.extract')
    def test_extract_from_file_with_text(self, mock_extract):
        """Test the convenience function with a text file."""
        mock_extract.return_value = "Extracted content"
        
        result = extract_from_file("test.txt")
        assert result == "Extracted content"
        mock_extract.assert_called_once_with("test.txt")
    
    def test_extract_from_file_real_file(self):
        """Test the convenience function with a real file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            test_content = "This is test content for extraction."
            f.write(test_content)
            f.flush()
            
            try:
                result = extract_from_file(f.name)
                assert isinstance(result, str)
                assert test_content in result
            finally:
                Path(f.name).unlink()


class TestArchitecturalBenefits:
    """Tests demonstrating architectural benefits of the interface."""
    
    def test_dependency_injection_pattern(self):
        """Test how the interface enables dependency injection."""
        
        class FileProcessor:
            def __init__(self, extractor: IExtractor):
                self.extractor = extractor
            
            def process(self, file_path: str) -> str:
                content = self.extractor.extract(file_path)
                return f"Processed: {content[:50]}..."
        
        # Can inject any extractor implementation
        text_processor = FileProcessor(TextExtractor())
        pdf_processor = FileProcessor(PDFExtractor())
        ocr_processor = FileProcessor(OCRExtractor())
        
        # All work the same way despite different implementations
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            f.flush()
            
            try:
                result = text_processor.process(f.name)
                assert result.startswith("Processed:")
                assert isinstance(result, str)
            finally:
                Path(f.name).unlink()
    
    def test_strategy_pattern(self):
        """Test how the interface enables strategy pattern."""
        
        class ExtractionStrategy:
            def __init__(self):
                self.extractor: IExtractor = TextExtractor()  # default
            
            def set_extractor(self, extractor: IExtractor):
                self.extractor = extractor
            
            def extract(self, file_path: str) -> str:
                return self.extractor.extract(file_path)
        
        strategy = ExtractionStrategy()
        
        # Can change strategy at runtime
        strategy.set_extractor(TextExtractor())
        strategy.set_extractor(PDFExtractor())
        strategy.set_extractor(OCRExtractor())
        
        # Interface ensures all work the same way
        assert hasattr(strategy.extractor, 'extract')
        assert isinstance(strategy.extractor, IExtractor) 
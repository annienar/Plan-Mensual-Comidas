"""
Recipe domain extractors.

This module contains the extractors for the recipe domain that follow
clean architecture principles. These extractors define the interfaces
and base classes that application layer extractors implement.

Domain extractors define the contracts for extraction operations
without depending on external infrastructure.
"""

from .ingredients import IngredientExtractor

from .base import BaseExtractor
from .metadata import MetadataExtractor
from .sections import SectionExtractor
__all__ = [
    "BaseExtractor", 
    "SectionExtractor", 
    "MetadataExtractor", 
    "IngredientExtractor"
]

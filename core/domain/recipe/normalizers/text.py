"""
Text normalizer for standardizing recipe text content.
"""
from typing import Dict, List, Any
import re

from .base import BaseNormalizer
import unicodedata
COOKING_ABBREVIATIONS = {'tbsp': 'tablespoon', 'tsp': 'teaspoon', 'oz':
    'ounce', 'lb': 'pound', 'qt': 'quart', 'gal': 'gallon', 'min': 'minute', 
    'hr': 'hour', 'temp': 'temperature', 'approx': 'approximately', 
    'approx.': 'approximately', 'appx': 'approximately', 'appx.':
    'approximately', 'w/': 'with', 'w / o': 'without', 'etc': 'etcetera', 
    'etc.': 'etcetera', 'i.e.': 'that is', 'e.g.': 'for example', 'vs':
    'versus', 'vs.': 'versus'}
COOKING_TERMS = {'al dente', 'au gratin', 'au jus', 'bain - marie', 
    'bechamel', 'bouillon', 'brunoise', 'chiffonade', 'confit', 'consomme', 
    'coulis', 'demi - glace', 'emulsify', 'julienne', 'mirepoix', 
    'mise en place', 'parboil', 'poach', 'puree', 'roux', 'sauté', 'sautée', 
    'sautéd', 'sautéed', 'simmer', 'sous vide', 'temper', 'zest'}

class TextNormalizer(BaseNormalizer):
    """Normalize text content for recipes."""

    def __init__(self: Any) -> None:
        """Initialize the normalizer with abbreviations and terms."""
        self.abbreviations = COOKING_ABBREVIATIONS
        self.cooking_terms = COOKING_TERMS

    def _normalize_whitespace(self: Any, text: str) -> str:
        """
        Normalize whitespace in text.
        """
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _normalize_special_chars(self: Any, text: str) -> str:
        """
        Normalize special characters in text.
        """
        text = unicodedata.normalize('NFKC', text)
        replacements = {'–': '-', '—': '-', '…': '...', '"': '"', '“': '"', '”': '"', '‘': "'", '’': "'", '°': ' degrees ', '½': '1 / 2', '¼': '1 / 4', '¾': '3 / 4', '⅓': '1 / 3', '⅔': '2 / 3'}
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _expand_abbreviations(self: Any, text: str) -> str:
        """
        Expand common cooking abbreviations.
        """
        words = text.split()
        expanded_words = []
        for word in words:
            if word.lower() in self.abbreviations:
                expanded_words.append(self.abbreviations[word.lower()])
            else:
                expanded_words.append(word)
        return ' '.join(expanded_words)

    def _preserve_cooking_terms(self: Any, text: str) -> str:
        """
        Preserve common cooking terms.
        """
        words = text.split()
        preserved_words = []
        for word in words:
            if word.lower() in self.cooking_terms:
                preserved_words.append(word)
            else:
                preserved_words.append(word.lower())
        return ' '.join(preserved_words)

    def normalize(self: Any, text: str) ->str:
        """
        Normalize text content.

        Args:
            text: Text to normalize

        Returns:
            Normalized text

        Raises:
            ValueError: If text is not a string
        """
        if not isinstance(text, str):
            raise ValueError('text must be a string')
        if not text:
            return ''
        text = self._normalize_special_chars(text)
        text = self._normalize_whitespace(text)
        text = self._expand_abbreviations(text)
        text = self._preserve_cooking_terms(text)
        return text

    def denormalize(self: Any, text: str) ->str:
        """
        Convert normalized text back to a more readable format.

        Args:
            text: Normalized text

        Returns:
            Denormalized text
        """
        if not text:
            return ''
        sentences = text.split('. ')
        sentences = [s.capitalize() for s in sentences]
        text = '. '.join(sentences)
        lines = text.split('\n')
        lines = [l.capitalize() for l in lines]
        text = '\n'.join(lines)
        return text

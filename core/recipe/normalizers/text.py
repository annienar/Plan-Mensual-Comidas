from .base import BaseNormalizer

class TextNormalizer(BaseNormalizer):
    def normalize(self, text: str) -> str:
        """Normalize text content. Stub implementation."""
        # TODO: Implement real text normalization logic
        return text.strip() 
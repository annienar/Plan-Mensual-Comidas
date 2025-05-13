from .base import BaseExtractor
import re
from typing import Any, Dict

class MetadataExtractor(BaseExtractor):
    def extract(self, content: str) -> Dict[str, Any]:
        """Extract metadata fields from recipe content."""
        return {
            'title': self._extract_title(content),
            'url': self._extract_url(content),
            'servings': self._extract_servings(content),
            'calories': self._extract_calories(content),
        }

    def _extract_title(self, content: str) -> str:
        for l in content.splitlines():
            if l.strip():
                return l.strip()
        return "Desconocido"

    def _extract_url(self, content: str) -> str:
        m = re.search(r"https?://\S+", content, re.IGNORECASE)
        return m.group(0) if m else "Desconocido"

    def _extract_servings(self, content: str) -> int | str:
        m = re.search(r"para\s*(\d+)\s*porciones?", content, re.IGNORECASE)
        return int(m.group(1)) if m else "Desconocido"

    def _extract_calories(self, content: str) -> int | str:
        m = re.search(r"calor[ií]as?:?\s*(\d+)", content, re.IGNORECASE)
        return int(m.group(1)) if m else "Desconocido" 
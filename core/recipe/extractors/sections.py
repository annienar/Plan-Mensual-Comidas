from typing import List, Dict
from .base import BaseExtractor
import re

class SectionExtractor(BaseExtractor):
    def extract(self, content: str) -> Dict[str, List[str]]:
        """Extract main recipe sections (ingredients, instructions, notes)."""
        sections = {
            'ingredients': [],
            'instructions': [],
            'notes': []
        }
        lines = [l.strip() for l in content.splitlines()]
        current = None
        for line in lines:
            if re.match(r"^ingredientes\b", line, re.IGNORECASE):
                current = 'ingredients'
                continue
            elif re.match(r"^(pasos?|preparaci[oó]n|paso a paso)", line, re.IGNORECASE):
                current = 'instructions'
                continue
            elif re.match(r"^(notas?|tips?)", line, re.IGNORECASE):
                current = 'notes'
                continue
            if current and line:
                sections[current].append(line)
        return sections 
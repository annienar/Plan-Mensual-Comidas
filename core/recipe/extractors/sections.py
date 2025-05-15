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
            # Section headers
            if re.match(r"^(ingredientes|ingredients)\b", line, re.IGNORECASE):
                current = 'ingredients'
                continue
            elif re.match(r"^(pasos?|preparaci[oó]n|steps?|instructions?)", line, re.IGNORECASE):
                current = 'instructions'
                continue
            elif re.match(r"^(notas?|tips?|notes?)", line, re.IGNORECASE):
                current = 'notes'
                continue
            # Only add lines to the current section if not a section header
            if current and line and not re.match(r"^(ingredientes|ingredients|pasos?|preparaci[oó]n|steps?|instructions?|notas?|tips?|notes?)\b", line, re.IGNORECASE):
                sections[current].append(line)
        return sections 
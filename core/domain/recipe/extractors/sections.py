from typing import List, Dict, Any
import re

from .base import BaseExtractor

class SectionExtractor(BaseExtractor):
    """Class SectionExtractor."""

    def extract(self: Any, content: str) ->Dict[str, List[str]]:
        """Extract main recipe sections (ingredients, instructions, notes)."""
        sections = {'ingredients': [], 'instructions': [], 'notes': []}
        lines = [l.strip() for l in content.splitlines()]
        current = None
        for line in lines:
            # Match ingredients section headers with various formats
            if re.match(r'^[-=*]*\s*(ingredientes|ingredients)\s*[-=*]*$', line, re.IGNORECASE):
                current = 'ingredients'
                continue
            elif re.match('^(ingredientes|ingredients)\\b', line, re.IGNORECASE):
                current = 'ingredients'
                continue
            # Match instructions section headers with various formats  
            elif re.match(r'^[-=*]*\s*(pasos?|preparaci[oó]n|steps?|instructions?)\s*[-=*]*$', line, re.IGNORECASE):
                current = 'instructions'
                continue
            elif re.match('^(pasos?|preparaci[oó]n|steps?|instructions?)', 
                line, re.IGNORECASE):
                current = 'instructions'
                continue
            # Match notes section headers
            elif re.match(r'^[-=*]*\s*(notas?|tips?|notes?|consejos?)\s*[-=*]*$', line, re.IGNORECASE):
                current = 'notes'
                continue
            elif re.match('^(notas?|tips?|notes?|consejos?)', line, re.IGNORECASE):
                current = 'notes'
                continue
            if current and line and not re.match(
                '^(ingredientes|ingredients|pasos?|preparaci[oó]n|steps?|instructions?|notas?|tips?|notes?)\\b'
                , line, re.IGNORECASE):
                sections[current].append(line)
        if not any(sections.values()):
            current = 'ingredients'
            for line in lines:
                if not line:
                    continue
                if re.match('^\\d+[\\.\\)]', line) or re.match('^[•\\-\\*]', 
                    line):
                    current = 'instructions'
                if re.match('^(nota|tip|consejo|sugerencia):', line, re.
                    IGNORECASE):
                    current = 'notes'
                sections[current].append(line)
        for section in sections:
            sections[section] = [line for line in sections[section] if line]
            sections[section] = list(dict.fromkeys(sections[section]))
        return sections

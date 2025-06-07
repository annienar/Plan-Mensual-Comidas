from datetime import datetime
from typing import Any, Dict, Optional, List, Union
import re

from .base import BaseExtractor
from dataclasses import dataclass
from enum import Enum

class RecipeType(Enum):
    """Class RecipeType."""
    DESAYUNO = 'Desayuno'
    ALMUERZO = 'Almuerzo'
    CENA = 'Cena'
    POSTRE = 'Postre'
    SNACK = 'Snack'
    BEBIDA = 'Bebida'
    OTRO = 'Otro'

@dataclass

class RecipeMetadata:
    """Class RecipeMetadata."""
    title: str
    url: Optional[str]
    porciones: Optional[int]
    calorias: Optional[int]
    tipo: Optional[str]
    tags: List[str]
    hecho: bool
    date: str
    dificultad: Optional[str]
    tiempo_preparacion: Optional[int]
    tiempo_coccion: Optional[int]
    tiempo_total: Optional[int]
    notas: Optional[str]

class MetadataExtractor(BaseExtractor):
    """Class MetadataExtractor."""

    def extract(self: Any, content: str) ->Dict[str, Any]:
        """Extract metadata fields from recipe content."""
        metadata = {'title': self._extract_title(content), 'url': self.
            _extract_url(content), 'porciones': self._extract_servings(
            content), 'calorias': self._extract_calories(content), 'tipo':
            self._extract_tipo(content), 'tags': self._extract_tags(content
), 'hecho': self._extract_hecho(content), 'date': self.
            _extract_date(content), 'dificultad': self._extract_difficulty(
            content), 'tiempo_preparacion': self._extract_prep_time(content
), 'tiempo_coccion': self._extract_cook_time(content), 
            'tiempo_total': self._extract_total_time(content), 'notas':
            self._extract_notes(content)}
        return self._validate_metadata(metadata)

    def _extract_title(self: Any, content: str) -> str:
        """Extract the recipe title.

        Args:
            content: The recipe content.

        Returns:
            The extracted title, or a generated concise title if not found.
        """
        lines = content.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('título:'):
                line = line[7:].strip()
            if line:
                return line
        for line in lines:
            line = line.strip()
            if line:
                return line
        return 'Receta generada'

    def _extract_url(self: Any, content: str) -> Optional[str]:
        """Extract source URL from content."""
        url_pattern = r'(?:URL|Fuente|Source):\s * (https?://\S+)'
        m = re.search(url_pattern, content, re.IGNORECASE)
        if m:
            return m.group(1)
        m = re.search(r'https?://\S+', content)
        return m.group(0) if m else None

    def _extract_servings(self: Any, content: str) -> Optional[int]:
        """Extract number of servings from content."""
        patterns = [r'(?:porciones|serves?|raciones):?\s * (\d+)', 
            r'para\s + (\d+)\s + (?:personas|porciones|servings)', 
            r'(\d+)\s + (?:porciones|servings|raciones)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    continue
        return None

    def _extract_calories(self: Any, content: str) -> Optional[int]:
        """Extract calorie count from content."""
        patterns = [r'calor[ií]as?:?\s * (\d+)', r'(\d+)\s * calor[ií]as', 
            r'kcal:?\s * (\d+)', r'(\d+)\s * kcal']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    continue
        return None

    def _extract_tipo(self: Any, content: str) -> Optional[str]:
        """Extract recipe type from content and map to RecipeType enum if possible."""
        patterns = [r'Tipo(?: de comida)?:\s * (.+)', r'Categoría:\s * (.+)', 
            r'Tipo:\s * (.+)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                tipo_raw = m.group(1).strip().lower()
                tipo_norm = tipo_raw.replace('á', 'a').replace('é', 'e'
).replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
                mapping = {'desayuno': 'DESAYUNO', 'almuerzo': 'ALMUERZO', 
                    'cena': 'CENA', 'postre': 'POSTRE', 'snack': 'SNACK', 
                    'bebida': 'BEBIDA', 'otro': 'OTRO'}
                enum_key = mapping.get(tipo_norm, None)
                if enum_key:
                    return RecipeType[enum_key].value
                try:
                    return RecipeType[tipo_norm.upper()].value
                except KeyError:
                    return tipo_raw.capitalize()
        return None

    def _extract_tags(self: Any, content: str) -> List[str]:
        """Extract recipe tags from content."""
        patterns = [r'(?:Tags|Etiquetas):\s * (.+)', 
            r'Palabras clave:\s * (.+)', r'Keywords:\s * (.+)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                tags = [tag.strip() for tag in m.group(1).split(', ') if tag
                    .strip()]
                return [tag.lower() for tag in tags]
        return []

    def _extract_hecho(self: Any, content: str) -> bool:
        """Extract 'hecho' status from content."""
        patterns = [r'Hecho:\s * (sí|si|true|x|1)', 
            r'Estado:\s * (completado|hecho|done)', r'✓\s * (?:Hecho|Completado)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                return True
        return False

    def _extract_date(self: Any, content: str) -> Optional[str]:
        """Extract date from content. Return None if not present."""
        patterns = [r'Date:\s * ([0 - 9]{4}-[0 - 9]{2}-[0 - 9]{2})', 
            r'Fecha:\s * ([0 - 9]{4}-[0 - 9]{2}-[0 - 9]{2})', 
            r'Fecha:\s * (\d{2}/\d{2}/\d{4})']
        for pattern in patterns:
            m = re.search(pattern, content)
            if m:
                date_str = m.group(1)
                if '/' in date_str:
                    day, month, year = date_str.split('/')
                    return f'{year}-{month}-{day}'
                return date_str
        return None

    def _extract_difficulty(self: Any, content: str) -> Optional[str]:
        """Extract difficulty level from content."""
        patterns = [r'Dificultad:\s * (.+)', r'Nivel:\s * (.+)', 
            r'Difficulty:\s * (.+)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                return m.group(1).strip().lower()
        return None

    def _extract_prep_time(self: Any, content: str) -> Optional[int]:
        """Extract preparation time in minutes."""
        patterns = [
            r'Tiempo de preparación:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Prep time:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Preparación:\s * (\d+)\s * (?:min|minutos|minutes)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    continue
        return None

    def _extract_cook_time(self: Any, content: str) -> Optional[int]:
        """Extract cooking time in minutes."""
        patterns = [
            r'Tiempo de cocción:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Cook time:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Cocción:\s * (\d+)\s * (?:min|minutos|minutes)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    continue
        return None

    def _extract_total_time(self: Any, content: str) -> Optional[int]:
        """Extract total time in minutes."""
        patterns = [r'Tiempo total:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Total time:\s * (\d+)\s * (?:min|minutos|minutes)', 
            r'Tiempo:\s * (\d+)\s * (?:min|minutos|minutes)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    continue
        return None

    def _extract_notes(self: Any, content: str) -> Optional[str]:
        """Extract recipe notes from content."""
        patterns = [r'Notas:\s * (.+?)(?:\n\n|\Z)', 
            r'Notes:\s * (.+?)(?:\n\n|\Z)', r'Consejos:\s * (.+?)(?:\n\n|\Z)']
        for pattern in patterns:
            m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if m:
                return m.group(1).strip()
        return None

    def _validate_metadata(self: Any, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean extracted metadata."""
        if not metadata['title']:
            metadata['title'] = 'Receta generada'
        if metadata['porciones'] is not None and metadata['porciones'] <= 0:
            metadata['porciones'] = None
        if metadata['calorias'] is not None and metadata['calorias'] <= 0:
            metadata['calorias'] = None
        if metadata['tipo']:
            try:
                metadata['tipo'] = RecipeType[metadata['tipo'].upper()].value
            except KeyError:
                metadata['tipo'] = RecipeType.OTRO.value
        metadata['tags'] = list(set(tag.lower() for tag in metadata['tags']))
        if metadata['tiempo_total'] is None:
            prep = metadata['tiempo_preparacion'] or 0
            cook = metadata['tiempo_coccion'] or 0
            if prep > 0 or cook > 0:
                metadata['tiempo_total'] = prep + cook
        return metadata

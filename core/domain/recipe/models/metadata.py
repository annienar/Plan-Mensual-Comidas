"""
Recipe metadata model.

This module contains the recipe metadata domain model.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, validator, constr, conint, conlist

class RecipeMetadata(BaseModel):
    """Recipe metadata model.

    Attributes:
        title: Recipe title
        porciones: Number of portions
        calorias: Calories per portion
        tipo: Recipe type
        tags: Recipe tags
        hecho: Completion status
        date: Recipe date
        dificultad: Difficulty level
        tiempo_preparacion: Preparation time in minutes
        tiempo_coccion: Cooking time in minutes
        tiempo_total: Total time in minutes
        notas: Additional notes
    """

    title: str = Field(
        default="Sin título", 
        min_length = 3, 
        max_length = 200, 
        description="Título de la receta"
)
    porciones: Optional[int] = Field(
        None, 
        gt = 0, 
        description="Número de porciones"
)
    calorias: Optional[int] = Field(
        None, 
        ge = 0, 
        description="Calorías por porción"
)
    tipo: Optional[str] = Field(
        None, 
        min_length = 1, 
        max_length = 50, 
        description="Tipo de receta"
)
    tags: List[str] = Field(
        default_factory=lambda: ["general"], 
        description="Etiquetas de la receta"
)
    hecho: bool = Field(
        False, 
        description="Estado de completado"
)
    date: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d"), 
        description="Fecha de la receta en formato YYYY - MM - DD"
)
    dificultad: Optional[str] = Field(
        None, 
        description="Nivel de dificultad"
)
    tiempo_preparacion: Optional[int] = Field(
        None, 
        ge = 0, 
        description="Tiempo de preparación en minutos"
)
    tiempo_coccion: Optional[int] = Field(
        None, 
        ge = 0, 
        description="Tiempo de cocción en minutos"
)
    tiempo_total: Optional[int] = Field(
        None, 
        gt = 0, 
        description="Tiempo total en minutos"
)
    notas: Optional[str] = Field(
        None, 
        description="Notas adicionales"
)
    url: str = Field(
        default="Desconocido",
        description="URL de origen de la receta"
)

    @validator('title')
    def validate_title(cls, v: str) -> str:
        """Validate recipe title.

        Args:
            v: Title to validate

        Returns:
            str: Validated title

        Raises:
            ValueError: If title is invalid
        """
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @validator('date')
    def validate_date(cls, v: str) -> str:
        """Validate recipe date.

        Args:
            v: Date to validate

        Returns:
            str: Validated date

        Raises:
            ValueError: If date is invalid
        """
        # Try multiple date formats
        formats = ["%Y-%m-%d", "%Y - %m - %d"]
        
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(v, fmt)
                # Always return in standard format
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        raise ValueError("Date must be in YYYY-MM-DD or YYYY - MM - DD format")
        return v

    @validator("dificultad")
    def validate_dificultad(cls, v: Optional[str]) -> Optional[str]:
        """Validate difficulty level.

        Args:
            v: Difficulty level to validate

        Returns:
            Optional[str]: Validated difficulty level

        Raises:
            ValueError: If difficulty level is invalid
        """
        if v is None:
            return None
            
        # Normalize input
        v_normalized = v.lower().strip()
        
        # Map English to Spanish
        english_to_spanish = {
            "easy": "Fácil",
            "medium": "Media", 
            "hard": "Difícil",
            "difficult": "Difícil"
        }
        
        # Check if it's English
        if v_normalized in english_to_spanish:
            return english_to_spanish[v_normalized]
            
        # Check if it's already Spanish (with or without accents)
        v_no_accents = v_normalized.replace('á', 'a').replace('í', 'i')
        spanish_levels = {
            "facil": "Fácil",
            "media": "Media", 
            "dificil": "Difícil"
        }
        
        if v_no_accents in spanish_levels:
            return spanish_levels[v_no_accents]
            
        # If already properly formatted Spanish, return as is
        if v in ["Fácil", "Media", "Difícil"]:
            return v

        raise ValueError(f"Invalid difficulty level: {v}. Must be one of ['easy', 'medium', 'hard'] or ['Fácil', 'Media', 'Difícil']")

    @validator('tags')
    def validate_tags(cls, v: List[str]) -> List[str]:
        """Validate tags.

        Args:
            v: Tags to validate

        Returns:
            List[str]: Validated tags

        Raises:
            ValueError: If tags are invalid
        """
        # If empty list, provide default tag
        if not v:
            v = ["general"]
            
        # Remove duplicates
        v = list(dict.fromkeys(v))

        # Sort tags
        v.sort()

        return v

    @validator('tiempo_total')
    def validate_tiempo_total(cls, v: Optional[int], values: Dict[str, Any]) -> Optional[int]:
        """Validate total time.

        Args:
            v: Total time to validate
            values: Other field values

        Returns:
            Optional[int]: Validated total time

        Raises:
            ValueError: If total time is invalid
        """
        if v is not None:
            prep_time = values.get('tiempo_preparacion', 0) or 0
            cook_time = values.get('tiempo_coccion', 0) or 0
            if v < prep_time + cook_time:
                raise ValueError("Total time must be greater than or equal to preparation time plus cooking time")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary.

        Returns:
            Dict[str, Any]: Metadata as dictionary
        """
        return {
            'title': self.title, 
            'porciones': self.porciones, 
            'calorias': self.calorias, 
            'tipo': self.tipo, 
            'tags': self.tags, 
            'hecho': self.hecho, 
            'date': self.date, 
            'dificultad': self.dificultad, 
            'tiempo_preparacion': self.tiempo_preparacion, 
            'tiempo_coccion': self.tiempo_coccion, 
            'tiempo_total': self.tiempo_total, 
            'notas': self.notas,
            'url': self.url
        }

    def to_markdown(self) -> str:
        """Convert metadata to markdown.

        Returns:
            str: Metadata as markdown
        """
        lines = []

        if self.porciones:
            lines.append(f"- **Porciones:** {self.porciones}")

        if self.calorias:
            lines.append(f"- **Calorías:** {self.calorias}")

        if self.tipo:
            lines.append(f"- **Tipo:** {self.tipo}")

        if self.tags:
            lines.append(f"- **Etiquetas:** {', '.join(self.tags)}")

        lines.append(f"- **Hecho:** {'Sí' if self.hecho else 'No'}")
        lines.append(f"- **Fecha:** {self.date}")

        if self.dificultad:
            lines.append(f"- **Dificultad:** {self.dificultad}")

        if self.tiempo_preparacion:
            lines.append(f"- **Tiempo de preparación:** {self.tiempo_preparacion} minutos")

        if self.tiempo_coccion:
            lines.append(f"- **Tiempo de cocción:** {self.tiempo_coccion} minutos")

        if self.tiempo_total:
            lines.append(f"- **Tiempo total:** {self.tiempo_total} minutos")

        if self.notas:
            lines.append(f"- **Notas:** {self.notas}")

        return "\n".join(lines)

    def to_notion_blocks(self) -> List[Dict[str, Any]]:
        """Convert metadata to Notion blocks.

        Returns:
            List[Dict[str, Any]]: Metadata as Notion blocks
        """
        blocks = []

        if self.porciones:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Porciones: "}}, 
                        {"type": "text", "text": {"content": str(self.porciones)}}
                    ]
                }
            })

        if self.calorias:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Calorías: "}}, 
                        {"type": "text", "text": {"content": str(self.calorias)}}
                    ]
                }
            })

        if self.tipo:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tipo: "}}, 
                        {"type": "text", "text": {"content": self.tipo}}
                    ]
                }
            })

        if self.tags:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Etiquetas: "}}, 
                        {"type": "text", "text": {"content": ", ".join(self.tags)}}
                    ]
                }
            })

        blocks.append({
            "object": "block", 
            "type": "bulleted_list_item", 
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Hecho: "}}, 
                    {"type": "text", "text": {"content": "Sí" if self.hecho else "No"}}
                ]
            }
        })

        blocks.append({
            "object": "block", 
            "type": "bulleted_list_item", 
            "bulleted_list_item": {
                "rich_text": [
                    {"type": "text", "text": {"content": "Fecha: "}}, 
                    {"type": "text", "text": {"content": self.date}}
                ]
            }
        })

        if self.dificultad:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Dificultad: "}}, 
                        {"type": "text", "text": {"content": self.dificultad}}
                    ]
                }
            })

        if self.tiempo_preparacion:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tiempo de preparación: "}}, 
                        {"type": "text", "text": {"content": f"{self.tiempo_preparacion} minutos"}}
                    ]
                }
            })

        if self.tiempo_coccion:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tiempo de cocción: "}}, 
                        {"type": "text", "text": {"content": f"{self.tiempo_coccion} minutos"}}
                    ]
                }
            })

        if self.tiempo_total:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Tiempo total: "}}, 
                        {"type": "text", "text": {"content": f"{self.tiempo_total} minutos"}}
                    ]
                }
            })

        if self.notas:
            blocks.append({
                "object": "block", 
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": "Notas: "}}, 
                        {"type": "text", "text": {"content": self.notas}}
                    ]
                }
            })

        return blocks

    def __str__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return (
            f"Metadata(porciones={self.porciones}, "
            f"calorias={self.calorias}, "
            f"tiempo_preparacion={self.tiempo_preparacion}, "
            f"tiempo_coccion={self.tiempo_coccion}, "
            f"dificultad='{self.dificultad}', "
            f"tags={self.tags})"
)

    def __repr__(self) -> str:
        """Get string representation.

        Returns:
            str: String representation
        """
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        """Check equality.

        Args:
            other: Object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, RecipeMetadata):
            return False

        return (
            self.porciones == other.porciones and
            self.calorias == other.calorias and
            self.tiempo_preparacion == other.tiempo_preparacion and
            self.tiempo_coccion == other.tiempo_coccion and
            self.dificultad == other.dificultad and
            self.tags == other.tags
)

    def __hash__(self) -> int:
        """Get hash.

        Returns:
            int: Hash value
        """
        return hash((
            self.porciones, 
            self.calorias, 
            self.tiempo_preparacion, 
            self.tiempo_coccion, 
            self.dificultad, 
            tuple(self.tags)
))

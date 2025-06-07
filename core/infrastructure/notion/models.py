"""
Type definitions and models for Notion integration.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional, TypedDict

from dataclasses import dataclass, field

class NotionBlock(TypedDict):
    """Base Notion block structure."""
    type: str
    content: Dict[str, Any]

class NotionTextBlock(NotionBlock):
    """Text block in Notion."""
    type: str  # "paragraph", "heading_1", "heading_2", "heading_3"
    content: Dict[str, Any]  # text, annotations, etc.

class NotionListBlock(NotionBlock):
    """List block in Notion."""
    type: str  # "bulleted_list_item", "numbered_list_item"
    content: Dict[str, Any]  # text, annotations, etc.

class NotionImageBlock(NotionBlock):
    """Image block in Notion."""
    type: str  # "image"
    content: Dict[str, Any]  # url, caption, etc.

class NotionPage(TypedDict):
    """Notion page structure."""
    id: str
    properties: Dict[str, Any]
    blocks: List[NotionBlock]

class NotionDatabase(TypedDict):
    """Notion database structure."""
    id: str
    title: str
    properties: Dict[str, Any]

@dataclass

class NotionConfig:
    """Configuration for Notion client."""
    api_key: str
    rate_limit: int = 3  # requests per second
    timeout: float = 30.0
    max_retries: int = 3
    retry_delay: float = 1.0

@dataclass

class NotionMetrics:
    """Metrics for Notion API usage."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rate_limit_hits: int = 0
    last_request_time: Optional[datetime] = None
    request_timestamps: List[datetime] = field(default_factory = list)

    def record_request(self, success: bool) -> None:
        """Record a request and its outcome.

        Args:
            success: Whether the request was successful
        """
        now = datetime.now()
        self.total_requests += 1
        if success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
        self.last_request_time = now
        self.request_timestamps.append(now)

        # Keep only last 1000 timestamps
        if len(self.request_timestamps) > 1000:
            self.request_timestamps = self.request_timestamps[-1000:]

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of the metrics.

        Returns:
            Dict[str, Any]: Metrics summary
        """
        return {
            "total_requests": self.total_requests, 
            "successful_requests": self.successful_requests, 
            "failed_requests": self.failed_requests, 
            "rate_limit_hits": self.rate_limit_hits, 
            "success_rate": self.successful_requests / self.total_requests if self.total_requests > 0 else 0, 
            "last_request_time": self.last_request_time.isoformat() if self.last_request_time else None, 
            "recent_requests": len(self.request_timestamps)
        }

@dataclass

class NotionPantryItem:
    name: str
    category: Optional[str] = None
    unit: Optional[str] = None
    stock: Optional[float] = None
    # Add more pantry properties as needed

@dataclass

class NotionIngredient:
    name: str
    pantry_id: Optional[str] = None  # Notion page ID of linked pantry item
    quantity: Optional[float] = None
    unit: Optional[str] = None
    receta_id: Optional[str] = None  # Notion page ID of linked recipe
    # Add more ingredient properties as needed

@dataclass

class NotionRecipe:
    title: str
    ingredient_ids: List[str]  # Notion page IDs of linked ingredients
    portions: Optional[int] = None
    calories: Optional[int] = None
    tags: Optional[List[str]] = None
    tipo: Optional[str] = None
    hecho: Optional[bool] = None
    date: Optional[str] = None
    dificultad: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    tiempo_coccion: Optional[int] = None
    tiempo_total: Optional[int] = None
    notas: Optional[str] = None
    url: Optional[str] = None
    ingredients: List[Any] = field(default_factory = list)  # List of ingredient objects
    instructions: List[str] = field(default_factory = list)  # List of preparation steps
    # Add more recipe properties as needed

# Add more fields as needed

"""
Base event module.

This module contains the base event class.
"""

from datetime import datetime
from typing import Any, Dict
from uuid import uuid4

class DomainEvent:
    """Base domain event class.

    Attributes:
        event_id: Unique event identifier
        occurred_on: When the event occurred
        event_type: Type of event
        metadata: Additional event metadata
    """

    def __init__(self, metadata: Dict[str, Any] = None):
        """Initialize the event.

        Args:
            metadata: Additional event metadata
        """
        self.event_id = str(uuid4())
        self.occurred_on = datetime.now()
        self.event_type = self.__class__.__name__
        self.metadata = metadata or {}

    def __str__(self) -> str:
        """Get string representation of the event.

        Returns:
            str: String representation
        """
        return (
            f"{self.event_type}("
            f"id={self.event_id}, "
            f"occurred_on={self.occurred_on.isoformat()}, "
            f"metadata={self.metadata}"
            f")"
)

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary.

        Returns:
            Dict[str, Any]: Event as dictionary
        """
        return {
            "event_id": self.event_id, 
            "occurred_on": self.occurred_on.isoformat(), 
            "event_type": self.event_type, 
            "metadata": self.metadata
        }

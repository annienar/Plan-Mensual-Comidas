from abc import ABC, abstractmethod
from typing import Any

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, content: str) -> Any:
        """Extract specific data from recipe content."""
        pass 
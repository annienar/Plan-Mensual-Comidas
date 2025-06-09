from typing import Any

from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Class BaseExtractor."""

    @abstractmethod
    def extract(self: Any, content: str) ->Any:
        """Extract specific data from recipe content."""
        pass

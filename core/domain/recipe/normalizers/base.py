from typing import Any

from abc import ABC, abstractmethod

class BaseNormalizer(ABC):
    """Class BaseNormalizer."""

    @abstractmethod
    def normalize(self: Any, data: Any) ->Any:
        """Normalize specific recipe data."""
        pass

    @abstractmethod
    def denormalize(self: Any, data: Any) ->Any:
        """Convert normalized data back to its original format."""
        pass

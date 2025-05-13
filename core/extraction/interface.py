from abc import ABC, abstractmethod

class IExtractor(ABC):
    @abstractmethod
    def extract(self, source_path: str) -> str:
        """Extract raw text from the given source file."""
        pass 
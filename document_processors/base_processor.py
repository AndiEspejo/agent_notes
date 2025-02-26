from abc import ABC, abstractmethod
from typing import List

class BaseDocumentProcessor(ABC):
    @abstractmethod
    def process(self, file_path: str) -> List[str]:
        """Process a document and return text chunks"""
        pass 
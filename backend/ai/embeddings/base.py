from abc import ABC, abstractmethod
from pgvector.vector import Vector

class BaseEmbedding(ABC):
    @abstractmethod
    def generate(self, text: str) -> Vector:
        pass
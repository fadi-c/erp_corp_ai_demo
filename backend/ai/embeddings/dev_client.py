from pgvector.vector import Vector
from .base import BaseEmbedding

class DevEmbedding(BaseEmbedding):
    MODEL_DIM = 1536

    def generate(self, text: str) -> Vector:
        import hashlib

        h = hashlib.sha256(text.encode("utf-8")).digest()
        floats = [((b / 255) * 2 - 1) for b in h]
        full_vector = (floats * (self.MODEL_DIM // len(floats) + 1))[:self.MODEL_DIM]

        return Vector(full_vector)
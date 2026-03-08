import requests
import os
from pgvector.vector import Vector
from .base import BaseEmbedding
from django.conf import settings

class LocalEmbedding(BaseEmbedding):
    SERVICE_URL = os.getenv("LOCAL_EMBEDDING_URL", "http://localhost:5000/embed")
    MODEL_DIM = 1536  

    def generate(self, text: str) -> Vector:
        try:
            resp = requests.post(
                self.SERVICE_URL,
                json={"text": text},
                timeout=5
            )
            resp.raise_for_status()
            data = resp.json()
            embedding = data["embedding"]

            if len(embedding) != self.MODEL_DIM:
                embedding = (embedding * (self.MODEL_DIM // len(embedding) + 1))[:self.MODEL_DIM]

            return Vector(embedding)
        except Exception as e:
            print(f"[LocalEmbedding] failed, fallback to DevEmbedding: {e}")
            from .dev_client import DevEmbedding
            return DevEmbedding().generate(text)
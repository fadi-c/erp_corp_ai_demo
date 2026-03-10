import os
from openai import OpenAI
from .base import BaseEmbedding
from pgvector.vector import Vector

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIEmbedding(BaseEmbedding):

    MODEL = "text-embedding-3-small"
    MODEL_DIM = 1536
    def generate(self, text: str) -> Vector:
        response = client.embeddings.create(
            model=self.MODEL,
            input=text
        )
        return Vector(response.data[0].embedding)
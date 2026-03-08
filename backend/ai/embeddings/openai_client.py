import os
from openai import OpenAI
from .base import BaseEmbedding

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIEmbedding(BaseEmbedding):

    MODEL = "text-embedding-3-small"

    def generate(self, text: str):
        response = client.embeddings.create(
            model=self.MODEL,
            input=text
        )
        return response.data[0].embedding
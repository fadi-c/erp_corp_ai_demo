import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class EmbeddingService:

    MODEL = "text-embedding-3-small"

    @staticmethod
    def generate(text: str):

        response = client.embeddings.create(
            model=EmbeddingService.MODEL,
            input=text
        )

        return response.data[0].embedding
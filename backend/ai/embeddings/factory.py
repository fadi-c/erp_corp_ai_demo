from django.conf import settings
from .openai_client import OpenAIEmbedding
from .dev_client import DevEmbedding
from .base import BaseEmbedding

class EmbeddingFactory:

    @staticmethod
    def get_embedding_service() -> BaseEmbedding:
        env = getattr(settings, "AI_EMBEDDINGS", "FAKE").upper()
        if env == "OPENAI":
            return OpenAIEmbedding()
        return DevEmbedding()
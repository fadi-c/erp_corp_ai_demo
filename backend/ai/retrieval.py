from typing import List
from pgvector.django import CosineDistance
from erp.models import InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory
from django.db.models import Prefetch

class RetrievalService:

    @staticmethod
    def search(question: str, limit: int = 30) -> List[InvoiceEmbedding]:

        question_embedding = EmbeddingFactory.get_embedding_service().generate(question)

        results = (
            InvoiceEmbedding.objects
            .annotate(distance=CosineDistance('embedding', question_embedding))
            .order_by('distance')
            .select_related("invoice", "invoice__customer")
            .prefetch_related("invoice__order_set__product")
            [:limit]
        )
        return list(results)
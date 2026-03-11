from typing import List
from pgvector.django import CosineDistance
from erp.models import InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory
from django.db.models import Prefetch
from erp.models import Order, Product

class RetrievalService:

    @staticmethod
    def search(question: str, limit: int = 30) -> List[InvoiceEmbedding]:

        question_embedding = EmbeddingFactory.get_embedding_service().generate(question)
        orders_prefetch = Prefetch(
            "invoice__order_set",  # InvoiceEmbedding.invoice.order_set
            queryset=Order.objects.select_related("product").only(
                "product__name", "product__category", "quantity", "price", "invoice_id"
            ),
            to_attr="prefetched_orders"
        )

        results = (
            InvoiceEmbedding.objects
            .annotate(distance=CosineDistance('embedding', question_embedding))
            .order_by('distance')
            .select_related("invoice", "invoice__customer")
            .prefetch_related(orders_prefetch)
            [:limit]
        )
        return list(results)
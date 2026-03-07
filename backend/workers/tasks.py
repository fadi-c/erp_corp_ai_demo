from celery import shared_task
from erp.models import Invoice, InvoiceEmbedding
from ai.embeddings import EmbeddingService


@shared_task
def generate_invoice_embedding(invoice_id: int):

    invoice = Invoice.objects.get(id=invoice_id)

    text = f"""
    Invoice description: {invoice.description}
    Amount: {invoice.amount}
    Margin: {invoice.margin}
    """

    embedding = EmbeddingService.generate(text)

    InvoiceEmbedding.objects.update_or_create(
        invoice=invoice,
        defaults={"embedding": embedding}
    )
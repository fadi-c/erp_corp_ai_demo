from celery import shared_task
from erp.models import Invoice, InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory


@shared_task
def generate_invoice_embedding(invoice_id: int):

    invoice = Invoice.objects.get(id=invoice_id)

    text = f"""
    Invoice description: {invoice.description}
    Amount: {invoice.amount}
    Margin: {invoice.margin}
    """

    embedding = EmbeddingFactory.get_embedding_service().generate(text)

    InvoiceEmbedding.objects.update_or_create(
        invoice=invoice,
        defaults={"embedding": embedding}
    )
@shared_task
def generate_missing_invoice_embeddings():
    invoices = Invoice.objects.filter(embedding__isnull=True)
    for invoice in invoices:
        text = f"""
        Invoice description: {invoice.description}
        Amount: {invoice.amount}
        Margin: {invoice.margin}
        """
        embedding = EmbeddingFactory.get_embedding_service().generate(text)
        InvoiceEmbedding.objects.update_or_create(
            invoice=invoice,
            defaults={"embedding": embedding}
        )
    return f"{invoices.count()} embeddings processed."
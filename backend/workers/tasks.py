from celery import shared_task
from erp.models import Invoice, InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory


@shared_task(bind=True)
def generate_invoice_embedding(self, invoice_id: int):

    try:
        invoice = (
            Invoice.objects
            .select_related("customer")
            .prefetch_related("order_set__product")
            .get(id=invoice_id)
        )
    except Invoice.DoesNotExist:
        print(f"[generate_invoice_embedding] Invoice {invoice_id} does not exist, skipping.")
        return f"Invoice {invoice_id} missing"

    orders = invoice.order_set.all()
    text = f"""
Invoice {invoice.id}
Customer: {invoice.customer.name} ({invoice.customer.industry})
Description: {invoice.description}
Amount: {invoice.amount}
Margin: {invoice.margin}
Date: {invoice.date}
Orders:
""" + "\n".join([f"- {o.product.name} ({o.product.category}): {o.quantity} units @ {o.price} EUR" for o in orders])

    embedding = EmbeddingFactory.get_embedding_service().generate(text)

    InvoiceEmbedding.objects.update_or_create(
        invoice=invoice,
        defaults={"embedding": embedding}
    )

    print(f"[generate_invoice_embedding] Invoice {invoice.id} embedding generated")
    return f"Invoice {invoice.id} embedding generated"


@shared_task(bind=True)
def generate_missing_invoice_embeddings(self):

    invoices = (
        Invoice.objects
        .filter(embedding__isnull=True)
        .select_related("customer")
        .prefetch_related("order_set__product")
    )

    embedding_service = EmbeddingFactory.get_embedding_service()
    count = 0

    for invoice in invoices:
        try:
            orders = invoice.order_set.all()
            text = f"""
Invoice {invoice.id}
Customer: {invoice.customer.name} ({invoice.customer.industry})
Description: {invoice.description}
Amount: {invoice.amount}
Margin: {invoice.margin}
Date: {invoice.date}
Orders:
""" + "\n".join([f"- {o.product.name} ({o.product.category}): {o.quantity} units @ {o.price} EUR" for o in orders])

            embedding = embedding_service.generate(text)

            InvoiceEmbedding.objects.update_or_create(
                invoice=invoice,
                defaults={"embedding": embedding}
            )
            count += 1
        except Exception as e:
            print(f"[generate_missing_invoice_embeddings] Failed for Invoice {invoice.id}: {e}")

    print(f"[generate_missing_invoice_embeddings] {count} embeddings processed.")
    return f"{count} embeddings processed."
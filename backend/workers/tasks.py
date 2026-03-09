from celery import shared_task
from erp.models import Invoice, InvoiceEmbedding
from ai.embeddings.factory import EmbeddingFactory
from observability.metrics import (
    missing_invoice_embeddings,
    celery_task_total,
    celery_task_duration
)
import time

@shared_task(bind=True)
def update_missing_embeddings_metric(self):
    count = Invoice.objects.filter(embedding__isnull=True).count()
    missing_invoice_embeddings.set(count)
    return count

@shared_task(bind=True)
def generate_invoice_embedding(self, invoice_id: int):
    start = time.time()
    try:
        invoice = (
            Invoice.objects
            .select_related("customer")
            .prefetch_related("order_set__product")
            .get(id=invoice_id)
        )
    except Invoice.DoesNotExist:
        celery_task_total.labels(task_name="generate_invoice_embedding", status="failure").inc()
        return f"Invoice {invoice_id} missing"

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
""" + "\n".join([
            f"- {o.product.name} ({o.product.category}): {o.quantity} units @ {o.price} EUR"
            for o in orders
        ])

        embedding = EmbeddingFactory.get_embedding_service().generate(text)

        InvoiceEmbedding.objects.update_or_create(
            invoice=invoice,
            defaults={"embedding": embedding}
        )

        celery_task_total.labels(task_name="generate_invoice_embedding", status="success").inc()
        return f"Invoice {invoice.id} embedding generated"

    except Exception as e:
        celery_task_total.labels(task_name="generate_invoice_embedding", status="failure").inc()
        raise e
    finally:
        celery_task_duration.labels(task_name="generate_invoice_embedding").observe(time.time() - start)


@shared_task(bind=True)
def generate_missing_invoice_embeddings(self):
    invoices = (
        Invoice.objects
        .filter(embedding__isnull=True)
        .select_related("customer")
        .prefetch_related("order_set__product")
    )

    embedding_service = EmbeddingFactory.get_embedding_service()
    processed_count = 0

    for invoice in invoices:
        start_invoice = time.time()
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
""" + "\n".join([
                f"- {o.product.name} ({o.product.category}): {o.quantity} units @ {o.price} EUR"
                for o in orders
            ])

            embedding = embedding_service.generate(text)

            InvoiceEmbedding.objects.update_or_create(
                invoice=invoice,
                defaults={"embedding": embedding}
            )

            celery_task_total.labels(task_name="generate_missing_invoice_embeddings", status="success").inc()
            processed_count += 1

        except Exception as e:
            celery_task_total.labels(task_name="generate_missing_invoice_embeddings", status="failure").inc()
            print(f"[generate_missing_invoice_embeddings] Failed for Invoice {invoice.id}: {e}")

        finally:
            celery_task_duration.labels(task_name="generate_missing_invoice_embeddings").observe(time.time() - start_invoice)

    # Update missing embeddings gauge
    missing_invoice_embeddings.set(
        Invoice.objects.filter(embedding__isnull=True).count()
    )

    print(f"[generate_missing_invoice_embeddings] {processed_count} embeddings processed.")
    return f"{processed_count} embeddings processed."
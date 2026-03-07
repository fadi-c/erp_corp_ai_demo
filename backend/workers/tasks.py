from celery import shared_task


@shared_task
def generate_embedding(invoice_id: int):
    print(f"Generating embedding for invoice {invoice_id}")
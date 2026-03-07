from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice
from workers.tasks import generate_invoice_embedding


@receiver(post_save, sender=Invoice)
def trigger_embedding(sender, instance, created, **kwargs):

    if created:
        generate_invoice_embedding.delay(instance.id)
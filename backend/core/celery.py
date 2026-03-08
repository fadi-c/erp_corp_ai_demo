import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("erp_ai")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "generate-invoice-embeddings-5m": {
        "task": "workers.tasks.generate_missing_invoice_embeddings",
        "schedule": crontab(minute="*/5"),
    },
}
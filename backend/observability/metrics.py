import os
import shutil
from prometheus_client import Counter, Gauge, Histogram

PROM_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", "/tmp/prometheus")

if os.path.exists(PROM_DIR):
    shutil.rmtree(PROM_DIR)

os.makedirs(PROM_DIR, exist_ok=True)


# API Metrics
api_requests = Counter(
    "api_requests_total",
    "Total API Requests",
    ["endpoint", "method", "status"]
)

api_latency = Histogram(
    "api_request_latency_seconds",
    "API request latency in seconds",
    ["endpoint", "method"]
)

# Invoice embeddings metrics
missing_invoice_embeddings = Gauge(
    "missing_invoice_embeddings_total",
    "Number of invoices missing embeddings"
)

# Celery tasks metrics
celery_task_total = Counter(
    "celery_task_total",
    "Total number of Celery tasks",
    ["task_name", "status"]
)

celery_task_duration = Histogram(
    "celery_task_duration_seconds",
    "Duration of Celery tasks in seconds",
    ["task_name"]
)
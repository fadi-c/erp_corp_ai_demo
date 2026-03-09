import os
import shutil
import threading

from prometheus_client import CollectorRegistry, multiprocess, start_http_server

PROM_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", "/tmp/prometheus")

if os.path.exists(PROM_DIR):
    shutil.rmtree(PROM_DIR)

os.makedirs(PROM_DIR, exist_ok=True)


def start_metrics_server(port=5556):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)

    start_http_server(port, registry=registry)
    print(f"[metrics] Celery beat metrics server started on port {port}")


threading.Thread(target=start_metrics_server, daemon=True).start()

os.system("celery -A core beat -l info")
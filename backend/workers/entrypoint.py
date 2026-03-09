import os
import threading
from prometheus_client import CollectorRegistry, multiprocess, start_http_server
import shutil
import os

PROM_DIR = "/tmp/prometheus"

if os.path.exists(PROM_DIR):
    shutil.rmtree(PROM_DIR)

os.makedirs(PROM_DIR, exist_ok=True)

def start_metrics_server(port=5555):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    start_http_server(port, registry=registry)
    print(f"[metrics] Prometheus multiprocess server started on {port}")

threading.Thread(target=start_metrics_server, daemon=True).start()

os.system("celery -A core worker -l info")
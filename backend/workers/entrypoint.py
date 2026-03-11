import os
import threading
import shutil

PROMETHEUS_MULTIPROC_DIR = os.environ.get("PROMETHEUS_MULTIPROC_DIR", "/tmp/prometheus")

os.environ["PROMETHEUS_MULTIPROC_DIR"] = PROMETHEUS_MULTIPROC_DIR

if os.path.exists(PROMETHEUS_MULTIPROC_DIR):
    shutil.rmtree(PROMETHEUS_MULTIPROC_DIR)

os.makedirs(PROMETHEUS_MULTIPROC_DIR, exist_ok=True)

from prometheus_client import CollectorRegistry, multiprocess, start_http_server


def start_metrics_server(port=5555):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    start_http_server(port, registry=registry)
    print(f"[metrics] Prometheus multiprocess server started on {port}")


threading.Thread(target=start_metrics_server, daemon=True).start()

os.system("celery -A core worker -l info")
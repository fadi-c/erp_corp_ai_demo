from prometheus_client import Counter

api_requests = Counter(
    "api_requests_total",
    "Total API Requests"
)
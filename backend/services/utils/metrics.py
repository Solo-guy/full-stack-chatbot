from prometheus_client import Counter, Histogram
from prometheus_client.exposition import generate_latest

REQUEST_COUNT = Counter('request_count', 'Total API requests', ['endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'API request latency', ['endpoint'])

def setup_metrics():
    """
    Setup Prometheus metrics.
    """
    def metrics_middleware(endpoint: str):
        REQUEST_COUNT.labels(endpoint=endpoint).inc()
        with REQUEST_LATENCY.labels(endpoint=endpoint).time():
            pass  # Giả lập thời gian xử lý

    return metrics_middleware

def get_metrics():
    """
    Get current metrics for Prometheus.
    """
    return generate_latest().decode('utf-8')
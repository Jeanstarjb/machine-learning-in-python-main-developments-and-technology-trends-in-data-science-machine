from prometheus_client import Counter, Gauge, Histogram

API_REQUESTS = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'http_status']
)

TRAINING_JOBS = Counter(
    'training_jobs_total',
    'Total training jobs executed',
    ['algorithm', 'status']
)

PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Prediction request latency',
    ['model_type']
)

SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_usage_percent',
    'Current system CPU usage percentage'
)

MODEL_MEMORY_USAGE = Gauge(
    'model_memory_usage_mb',
    'Memory usage by ML models',
    ['model_id']
)

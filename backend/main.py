from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from routers import data_router, model_router, preprocessing_router, training_router, evaluation_router, deployment_router, auth_router
from core.config import settings
from core.monitoring.metrics import API_REQUESTS, SYSTEM_CPU_USAGE
import psutil
import time

app = FastAPI(title="ML Platform API",
              description="End-to-end machine learning platform",
              version="0.1.0")

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process = psutil.Process()
    SYSTEM_CPU_USAGE.set(psutil.cpu_percent())
    
    API_REQUESTS.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()
    
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(data_router, prefix=settings.api_prefix)
app.include_router(model_router, prefix=settings.api_prefix)
app.include_router(preprocessing_router, prefix=settings.api_prefix)
app.include_router(training_router, prefix=settings.api_prefix)
app.include_router(evaluation_router, prefix=settings.api_prefix)
app.include_router(deployment_router, prefix=settings.api_prefix)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data_router, model_router, preprocessing_router, training_router, evaluation_router, deployment_router, auth_router
from core.config import settings
import os
from database.session import engine
from models.dataset_metadata import DatasetMetadata

app = FastAPI(title="ML Platform API",
              description="End-to-end machine learning platform",
              version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(data_router.router)
app.include_router(model_router.router)
app.include_router(preprocessing_router.router)
app.include_router(training_router.router)
app.include_router(evaluation_router.router)
app.include_router(deployment_router.router)

@app.on_event("startup")
async def startup_event():
    DatasetMetadata.metadata.create_all(bind=engine)
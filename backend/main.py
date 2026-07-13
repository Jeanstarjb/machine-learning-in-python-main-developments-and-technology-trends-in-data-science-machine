from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import data_router, model_router

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

app.include_router(data_router.router)
app.include_router(model_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

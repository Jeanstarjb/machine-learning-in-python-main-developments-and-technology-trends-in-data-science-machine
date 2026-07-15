from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# Model loading
MODEL_DIR = os.getenv("MODEL_DIR", "./models")
model = None

@app.on_event("startup")
async def load_model():
    global model
    model_path = os.path.join(MODEL_DIR, "model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found")
    model = joblib.load(model_path)

class PredictionRequest(BaseModel):
    data: list

@app.post("/predict")
async def predict(payload: PredictionRequest):
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        input_data = pd.DataFrame(payload.data)
        predictions = model.predict(input_data)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")
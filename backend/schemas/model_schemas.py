from pydantic import BaseModel, Field
from typing import Literal, Dict, Any

class TrainingConfig(BaseModel):
    algorithm: Literal['linear', 'decision_tree', 'dnn', 'cnn']
    problem_type: Literal['regression', 'classification']
    test_size: float = Field(0.2, ge=0.1, le=0.3)
    random_state: int = 42
    params: Dict[str, Any] = {}

class TrainingResponse(BaseModel):
    job_id: str
    status: str
    metrics: Dict[str, float] = {}
    model_path: str = None
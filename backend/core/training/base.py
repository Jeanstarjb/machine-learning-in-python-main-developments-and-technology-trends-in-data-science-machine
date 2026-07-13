from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import os
from core.config import settings

class BaseTrainer(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.metrics = {}

    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series):
        pass

    def evaluate(self, X: pd.DataFrame, y: pd.Series):
        predictions = self.model.predict(X)
        if self.config['problem_type'] == 'regression':
            self.metrics['mse'] = mean_squared_error(y, predictions)
        else:
            self.metrics['accuracy'] = accuracy_score(y, predictions)
        return self.metrics

    def save_model(self, job_id: str):
        model_path = os.path.join(settings.model_dir, f"{job_id}.joblib")
        os.makedirs(settings.model_dir, exist_ok=True)
        joblib.dump(self.model, model_path)
        return model_path
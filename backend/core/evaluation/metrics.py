import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from typing import Dict, Any

class EvaluationMetrics:
    @staticmethod
    def calculate_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray = None) -> Dict[str, Any]:
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='weighted', zero_division=0),
            "recall": recall_score(y_true, y_pred, average='weighted', zero_division=0),
            "f1_score": f1_score(y_true, y_pred, average='weighted', zero_division=0),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
        }
        
        if y_proba is not None:
            metrics["roc_auc"] = roc_auc_score(y_true, y_proba, multi_class='ovr')
        
        return metrics

    @staticmethod
    def calculate_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        metrics = {
            "mse": np.mean((y_true - y_pred) ** 2),
            "mae": np.mean(np.abs(y_true - y_pred)),
            "rmse": np.sqrt(np.mean((y_true - y_pred) ** 2))
        }
        return metrics
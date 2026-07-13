import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List

class EvaluationVisualization:
    @staticmethod
    def plot_confusion_matrix(cm: np.ndarray, class_names: List[str], output_path: str):
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted Labels')
        plt.ylabel('True Labels')
        plt.title('Confusion Matrix')
        plt.savefig(output_path)
        plt.close()

    @staticmethod
    def plot_metric_trend(metric_values: List[float], metric_name: str, output_path: str):
        plt.figure(figsize=(10, 6))
        plt.plot(metric_values, marker='o', label=metric_name)
        plt.title(f'{metric_name} Over Epochs')
        plt.xlabel('Epoch')
        plt.ylabel(metric_name)
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()
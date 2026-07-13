from .base import BaseTrainer
from sklearn.linear_model import LinearRegression, LogisticRegression
import pandas as pd

class LinearRegressionTrainer(BaseTrainer):
    def train(self, X: pd.DataFrame, y: pd.Series):
        if self.config['problem_type'] == 'regression':
            self.model = LinearRegression(**self.config.get('params', {}))
        else:
            self.model = LogisticRegression(**self.config.get('params', {}))
        self.model.fit(X, y)
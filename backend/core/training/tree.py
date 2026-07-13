from .base import BaseTrainer
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
import pandas as pd

class DecisionTreeTrainer(BaseTrainer):
    def train(self, X: pd.DataFrame, y: pd.Series):
        if self.config['problem_type'] == 'regression':
            self.model = DecisionTreeRegressor(**self.config.get('params', {}))
        else:
            self.model = DecisionTreeClassifier(**self.config.get('params', {}))
        self.model.fit(X, y)
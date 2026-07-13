from .base import BaseTrainer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import pandas as pd

class DNNTrainer(BaseTrainer):
    def train(self, X: pd.DataFrame, y: pd.Series):
        self.model = Sequential()
        for layer in self.config['layers']:
            self.model.add(Dense(**layer))
        
        self.model.compile(**self.config['compile_params'])
        self.model.fit(X, y, **self.config['fit_params'])
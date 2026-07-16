import pytest
from pandas import DataFrame
from numpy import array
from core.training import get_trainer

def test_linear_regression_training():
    X = DataFrame({'feature': [1, 2, 3, 4, 5]})
    y = array([2, 4, 6, 8, 10])
    config = {
        'problem_type': 'regression',
        'params': {}
    }
    trainer = get_trainer('linear', config)
    trainer.train(X, y)
    assert trainer.model is not None
    assert trainer.metrics['mse'] < 0.1

def test_dnn_training():
    X = DataFrame({'feature': [0.1, 0.2, 0.3, 0.4, 0.5]})
    y = array([0, 1, 0, 1, 0])
    config = {
        'problem_type': 'classification',
        'layers': [
            {'units': 4, 'activation': 'relu'},
            {'units': 1, 'activation': 'sigmoid'}
        ],
        'compile_params': {'optimizer': 'adam', 'loss': 'binary_crossentropy'},
        'fit_params': {'epochs': 10, 'verbose': 0}
    }
    trainer = get_trainer('dnn', config)
    trainer.train(X, y)
    assert isinstance(trainer.model, Sequential)
    assert len(trainer.model.layers) == 2

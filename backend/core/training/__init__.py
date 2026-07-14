from .linear import LinearRegressionTrainer
from .tree import DecisionTreeTrainer
from .dnn import DNNTrainer

def get_trainer(algorithm: str, config: dict):
    if algorithm == 'linear':
        return LinearRegressionTrainer(config)
    elif algorithm == 'decision_tree':
        return DecisionTreeTrainer(config)
    elif algorithm == 'dnn':
        return DNNTrainer(config)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
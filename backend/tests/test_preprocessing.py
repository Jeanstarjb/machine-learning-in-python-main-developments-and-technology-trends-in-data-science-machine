import pytest
from pandas import DataFrame
import numpy as np
from core.preprocessing.pipeline import PreprocessingPipeline

@pytest.fixture
def sample_data():
    return DataFrame({
        'numeric': [1, 2, np.nan, 4, 5],
        'categorical': ['A', 'B', 'A', np.nan, 'C']
    })

def test_missing_value_handling(sample_data):
    config = {'handle_missing': {'strategy': 'mean', 'columns': ['numeric']}}
    pipeline = PreprocessingPipeline()
    result = pipeline.transform(sample_data, config)
    assert result['numeric'].isna().sum() == 0
    assert round(result['numeric'].mean(), 2) == 3.0

def test_categorical_encoding(sample_data):
    config = {
        'encode_categorical': {
            'strategy': 'onehot',
            'columns': ['categorical'],
            'handle_unknown': 'ignore'
        }
    }
    pipeline = PreprocessingPipeline()
    result = pipeline.transform(sample_data, config)
    assert 'categorical_A' in result.columns
    assert 'categorical_B' in result.columns
    assert result.shape[1] == 4

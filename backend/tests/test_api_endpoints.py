from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import pytest

client = TestClient(app)

@patch('core.cloud_storage.S3Client')
def test_dataset_upload(mock_s3):
    mock_s3.return_value.upload_file.return_value = 's3://bucket/test.csv'
    response = client.post(
        '/api/v1/datasets/upload',
        files={'file': ('test.csv', b'content')},
        headers={'Authorization': 'Bearer testtoken'}
    )
    assert response.status_code == 201
    assert 's3://bucket/test.csv' in response.json()['location']

@patch('core.security.get_db')
def test_model_training_flow(mock_db):
    training_payload = {
        'algorithm': 'linear',
        'dataset_id': 1,
        'config': {'problem_type': 'regression'}
    }
    response = client.post(
        '/api/v1/models/train',
        json=training_payload,
        headers={'Authorization': 'Bearer testtoken'}
    )
    assert response.status_code == 202
    assert 'job_id' in response.json()

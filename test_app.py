import os
import sys
import pytest
from unittest.mock import patch, MagicMock
import numpy as np

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Mock the model loading before importing app
@pytest.fixture(autouse=True)
def mock_dependencies(monkeypatch):
    """Mock all external dependencies before importing app"""
    # Create mock prediction and label
    mock_prediction = np.array([0])  # low risk prediction
    mock_label = 'low risk'
    
    # Create mock classes with proper numpy arrays
    class MockModel:
        def predict(self, X):
            return mock_prediction

    class MockScaler:
        def transform(self, X):
            # Ensure X is a numpy array
            X = np.array(X) if not isinstance(X, np.ndarray) else X
            return np.array([[1.0] * X.shape[1]])

    class MockEncoder:
        def inverse_transform(self, X):
            return np.array([mock_label])

    # Patch joblib.load before importing app
    def mock_load(filename):
        if 'best_stacking_model' in filename:
            return MockModel()
        elif 'scaler' in filename:
            return MockScaler()
        elif 'label_encoder' in filename:
            return MockEncoder()
        raise FileNotFoundError(f"Mock cannot find {filename}")

    # Use monkeypatch to avoid issues with pickle loading
    monkeypatch.setattr('joblib.load', mock_load)
    
    return mock_label

# Import app after setting up mocks
from app import app

@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200

def test_prediction_endpoint_success(client, mock_dependencies):
    """Test the prediction endpoint with valid data"""
    test_data = {
        'Age': 25,
        'SystolicBP': 120,
        'DiastolicBP': 80,
        'BS': 6.0,
        'BodyTemp': 37.0,
        'HeartRate': 75
    }
    response = client.post('/predict', data=test_data)
    assert response.status_code == 200
    assert mock_dependencies.encode() in response.data

def test_prediction_endpoint_invalid_data(client):
    """Test the prediction endpoint with invalid data"""
    test_data = {
        'Age': 'invalid',
        'SystolicBP': 120,
        'DiastolicBP': 80,
        'BS': 6.0,
        'BodyTemp': 37.0,
        'HeartRate': 75
    }
    response = client.post('/predict', data=test_data)
    assert response.status_code == 200  # We return 200 with error message
    assert b"invalid literal for int()" in response.data 
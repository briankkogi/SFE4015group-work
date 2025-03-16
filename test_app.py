import pytest
from unittest.mock import patch, MagicMock
import numpy as np

# Mock the model and related components before importing app
mock_prediction = np.array([0])  # low risk prediction
mock_label = 'low risk'

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('joblib.load') as mock_load:
        # Create mock objects
        mock_model = MagicMock()
        mock_model.predict.return_value = mock_prediction
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]])
        
        mock_encoder = MagicMock()
        mock_encoder.inverse_transform.return_value = np.array([mock_label])
        
        # Configure mock to return different objects for different model files
        def load_side_effect(filename):
            if 'best_stacking_model' in filename:
                return mock_model
            elif 'scaler' in filename:
                return mock_scaler
            elif 'label_encoder' in filename:
                return mock_encoder
            raise FileNotFoundError(f"Mock cannot find {filename}")
            
        mock_load.side_effect = load_side_effect
        yield mock_load

# Import app after setting up mocks
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200

def test_prediction_endpoint_success(client):
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
    assert mock_label.encode() in response.data

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
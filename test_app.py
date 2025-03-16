import pytest
from unittest.mock import patch
import numpy as np

# Mock the model and related components
@pytest.fixture(autouse=True)
def mock_model():
    with patch('joblib.load') as mock_load:
        # Create mock objects for model, scaler, and label_encoder
        mock_model = mock_load.return_value
        mock_model.predict.return_value = np.array([0])  # Mock prediction
        yield mock_load

# Import app after setting up mocks to avoid loading real models
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_prediction_endpoint(client):
    """Test the prediction endpoint with valid data"""
    test_data = {
        'Age': 25,
        'SystolicBP': 120,
        'DiastolicBP': 80,
        'BS': 6.0,
        'BodyTemp': 37.0,
        'HeartRate': 75
    }
    rv = client.post('/predict', data=test_data)
    assert rv.status_code == 200 
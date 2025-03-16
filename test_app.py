import pytest
from app import app
import json

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
import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_home(client):
    """Test the home endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Flask ML API is running!"


def test_predict_valid(client):
    """Test prediction with valid input"""
    response = client.post("/predict", json={"ad_spend": 300})
    assert response.status_code == 200
    data = response.get_json()
    assert "predicted_units_sold" in data
    # Rough sanity check: prediction should be around 40
    assert 35 <= data["predicted_units_sold"] <= 45


def test_predict_missing_value(client):
    """Test prediction with missing ad_spend"""
    response = client.post("/predict", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health():
    response = client.get("/")
    print("Health check:", response.json())
    assert response.status_code == 200

def test_sarima():
    response = client.post("/predict/sarima", json={"n_periods": 5})
    print("SARIMA response:", response.json())
    assert response.status_code == 200

def test_svm():
    response = client.post("/predict/svm", json={"features": [100.5, 101.2, 99.8, 100.0, 50000.0, 10.5]})
    print("SVM response:", response.json())
    assert response.status_code == 200

if __name__ == "__main__":
    print("Running tests...")
    test_health()
    test_sarima()
    test_svm()
    print("All tests passed!")

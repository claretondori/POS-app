from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    end_point = "/" #arrange
    response = client.get(end_point) #act
    assert response.status_code == 200 #assert
   

# Test functions 
import pytest
from fastapi.testclient import TestClient  
from main import app


@pytest.fixture
def test_app():
    return app


def test_index(test_app):
    client = TestClient(test_app)
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_signup(test_app):
    client = TestClient(test_app)
    response = client.post("/signup/", data={"username": "test_user", "password": "password"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "test_user" in response.text

def test_duplicate_signup(test_app):
    client = TestClient(test_app)
    response = client.post("/signup/", data={"username": "test_user", "password": "password"})
    assert response.status_code == 400
    assert "Username already registered" in response.text

def test_login(test_app):
    client = TestClient(test_app)
    response = client.post("/login/", data={"username": "test_user", "password": "password"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "test_user" in response.text

def test_gemini_api(test_app):
    client = TestClient(test_app)
    prompt = "Generate a caption for this image."
    img_url = "https://example.com/image.jpg"
    response = client.post("/api/gemini", json={"prompt": prompt, "img_url": img_url})
    assert response.status_code == 200
    assert "text/markdown" in response.headers["content-type"]
    assert "Generated caption" in response.text  # Customize based on expected output


if __name__ == "__main__":
    pytest.main()

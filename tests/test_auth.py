from fastapi.testclient import TestClient


def test_google_login(client: TestClient):
    response = client.get("/auth/login/google", follow_redirects=False)
    assert response.status_code == 307
    assert "accounts.google.com" in response.headers["location"]


def test_microsoft_login(client: TestClient):
    response = client.get("/auth/login/microsoft", follow_redirects=False)
    assert response.status_code == 307
    assert "login.microsoftonline.com" in response.headers["location"]
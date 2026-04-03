import uuid


def test_register_success(client):
    email = f"register-{uuid.uuid4()}@example.com"
    payload = {"email": email, "password": "Password123"}

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == email
    assert "id" in body


def test_login_success(client):
    email = f"login-{uuid.uuid4()}@example.com"
    password = "Password123"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_invalid_password(client):
    email = f"invalid-pass-{uuid.uuid4()}@example.com"
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123"})

    response = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPass999"})

    assert response.status_code == 401

import uuid


def test_register_success(client):
    email = f"register-{uuid.uuid4()}@example.com"
    payload = {"email": email, "password": "Password123!"}

    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == email
    assert "id" in body


def test_login_success(client):
    email = f"login-{uuid.uuid4()}@example.com"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"


def test_refresh_success(client):
    email = f"refresh-{uuid.uuid4()}@example.com"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={"email": email, "password": password})

    login_response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    refresh_response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    refresh_body = refresh_response.json()
    assert "access_token" in refresh_body
    assert refresh_body["refresh_token"] == refresh_token
    assert refresh_body["token_type"] == "bearer"


def test_register_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "not-an-email", "password": "Password123!"},
    )

    assert response.status_code == 422


def test_register_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": f"weak-{uuid.uuid4()}@example.com", "password": "password123"},
    )

    assert response.status_code == 422


def test_login_invalid_password(client):
    email = f"invalid-pass-{uuid.uuid4()}@example.com"
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})

    response = client.post("/api/v1/auth/login", json={"email": email, "password": "WrongPass999"})

    assert response.status_code == 401

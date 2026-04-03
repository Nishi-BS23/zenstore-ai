def test_create_product(client, auth_headers):
    payload = {
        "name": "Test Product",
        "price": 99.99,
        "details": "Created from test",
    }

    response = client.post("/api/v1/products", json=payload, headers=auth_headers)

    assert response.status_code == 202


def test_get_product_by_id(client, auth_headers):
    payload = {
        "name": "Get By ID Product",
        "price": 149.50,
        "details": "Should be retrievable",
    }

    create_response = client.post("/api/v1/products", json=payload, headers=auth_headers)
    assert create_response.status_code == 202

    list_response = client.get("/api/v1/products", headers=auth_headers)
    assert list_response.status_code == 200
    products = list_response.json()

    product_id = next(p["id"] for p in products if p["name"] == payload["name"])

    get_response = client.get(f"/api/v1/products/{product_id}", headers=auth_headers)
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["id"] == product_id
    assert body["name"] == payload["name"]


def test_unauthorized_access(client):
    response = client.get("/api/v1/products")

    assert response.status_code == 401

def test_bulk_upload_csv(client, auth_headers):
    csv_content = (
        "name,price,details,description,category\n"
        "Keyboard,59.99,Mechanical keyboard,RGB keyboard,Accessories\n"
        "Mouse,29.50,Wireless mouse,Ergonomic mouse,Accessories\n"
    )

    response = client.post(
        "/api/v1/products/bulk",
        files={"file": ("products.csv", csv_content, "text/csv")},
        headers=auth_headers,
    )

    assert response.status_code == 202
    body = response.json()
    assert "job_id" in body
    assert isinstance(body["job_id"], str)
    assert body["job_id"]
    assert "message" in body
    assert "Bulk upload accepted" in body["message"]


def test_bulk_upload_invalid_file_type(client, auth_headers):
    response = client.post(
        "/api/v1/products/bulk",
        files={"file": ("products.txt", "not,csv,data", "text/plain")},
        headers=auth_headers,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a CSV file"

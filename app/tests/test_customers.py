def test_create_customer_success(client):
    response = client.post(
        "/customers/",
        json={"full_name": "Amina Njoroge", "phone": "0712345678", "email": "amina@example.com"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["full_name"] == "Amina Njoroge"
    assert body["loyalty_points"] == 0


def test_create_customer_invalid_email_returns_422(client):
    response = client.post(
        "/customers/",
        json={"full_name": "Brian Otieno", "email": "not-an-email"},
    )
    assert response.status_code == 422


def test_create_customer_missing_full_name_returns_422(client):
    response = client.post("/customers/", json={"phone": "0700000000"})
    assert response.status_code == 422


def test_get_customer_not_found_returns_404(client):
    response = client.get("/customers/999")
    assert response.status_code == 404


def test_update_customer_success(client):
    created = client.post("/customers/", json={"full_name": "Wanjiru Kamau"}).json()
    response = client.put(
        f"/customers/{created['customer_id']}",
        json={"loyalty_points": 50},
    )
    assert response.status_code == 200
    assert response.json()["loyalty_points"] == 50


def test_delete_customer_success(client):
    created = client.post("/customers/", json={"full_name": "Kevin Mwangi"}).json()
    response = client.delete(f"/customers/{created['customer_id']}")
    assert response.status_code == 204
    response = client.get(f"/customers/{created['customer_id']}")
    assert response.status_code == 404


def test_list_customers_returns_all_created(client):
    client.post("/customers/", json={"full_name": "Faith Chebet"})
    response = client.get("/customers/")
    assert response.status_code == 200
    assert any(c["full_name"] == "Faith Chebet" for c in response.json())


import pytest


@pytest.fixture
def cashier_id(client):
    response = client.post(
        "/users/",
        json={"username": "sales_cashier", "full_name": "Sales Cashier", "password": "cashierpass1"},
    )
    return response.json()["user_id"]


def test_create_sale_success(client, cashier_id):
    response = client.post("/sales/", json={"user_id": cashier_id})
    assert response.status_code == 201
    body = response.json()
    assert body["user_id"] == cashier_id
    assert body["status"] == "completed"
    assert float(body["total_amount"]) == 0


def test_create_sale_nonexistent_user_returns_400(client):
    response = client.post("/sales/", json={"user_id": 999})
    assert response.status_code == 400


def test_create_sale_nonexistent_customer_returns_400(client, cashier_id):
    response = client.post("/sales/", json={"user_id": cashier_id, "customer_id": 999})
    assert response.status_code == 400


def test_get_sale_not_found_returns_404(client):
    response = client.get("/sales/999")
    assert response.status_code == 404


def test_update_sale_status_success(client, cashier_id):
    created = client.post("/sales/", json={"user_id": cashier_id}).json()
    response = client.put(f"/sales/{created['sale_id']}", json={"status": "voided"})
    assert response.status_code == 200
    assert response.json()["status"] == "voided"


def test_delete_sale_success(client, cashier_id):
    created = client.post("/sales/", json={"user_id": cashier_id}).json()
    response = client.delete(f"/sales/{created['sale_id']}")
    assert response.status_code == 204
    response = client.get(f"/sales/{created['sale_id']}")
    assert response.status_code == 404


def test_list_sales_returns_all_created(client, cashier_id):
    client.post("/sales/", json={"user_id": cashier_id})
    response = client.get("/sales/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


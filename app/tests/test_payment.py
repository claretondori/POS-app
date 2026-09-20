import pytest


@pytest.fixture
def sale_with_total(authed_client):
    """A sale carrying a KES 1000.00 total (2 hammers @ 500 each), so
    payment tests have real amounts to work with and to exceed."""
    user_id = authed_client.post(
        "/users/",
        json={"username": "pay_cashier", "full_name": "Pay Cashier", "password": "paycashier1"},
    ).json()["user_id"]
    category_id = authed_client.post("/categories/", json={"name": "Hardware"}).json()["category_id"]
    product = authed_client.post(
        "/products/",
        json={
            "sku": "HAM-001",
            "name": "Hammer",
            "category_id": category_id,
            "unit_price": "500.00",
            "cost_price": "300.00",
            "quantity_in_stock": 20,
        },
    ).json()
    sale = authed_client.post("/sales/", json={"user_id": user_id}).json()
    authed_client.post(
        "/sale-items/",
        json={"sale_id": sale["sale_id"], "product_id": product["product_id"], "quantity": 2},
    )
    return sale["sale_id"]


def test_create_payment_success(authed_client, sale_with_total):
    response = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "500.00"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["payment_method"] == "cash"
    assert float(body["amount_paid"]) == 500.00


def test_create_payment_exceeding_amount_owed_returns_400(authed_client, sale_with_total):
    response = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "5000.00"},
    )
    assert response.status_code == 400


def test_create_payment_nonexistent_sale_returns_400(authed_client):
    response = authed_client.post(
        "/payments/",
        json={"sale_id": 999, "payment_method": "cash", "amount_paid": "10.00"},
    )
    assert response.status_code == 400


def test_create_payment_negative_amount_returns_422(authed_client, sale_with_total):
    response = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "card", "amount_paid": "-5.00"},
    )
    assert response.status_code == 422


def test_create_payment_invalid_method_returns_422(authed_client, sale_with_total):
    response = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "bitcoin", "amount_paid": "10.00"},
    )
    assert response.status_code == 422


def test_multiple_payments_cannot_exceed_total(authed_client, sale_with_total):
    first = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "700.00"},
    )
    assert first.status_code == 201
    second = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "mobile_money", "amount_paid": "400.00"},
    )
    assert second.status_code == 400


def test_get_payment_not_found_returns_404(authed_client):
    response = authed_client.get("/payments/999")
    assert response.status_code == 404


def test_update_payment_amount_success(authed_client, sale_with_total):
    created = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "200.00"},
    ).json()
    response = authed_client.put(
        f"/payments/{created['payment_id']}",
        json={"amount_paid": "300.00"},
    )
    assert response.status_code == 200
    assert float(response.json()["amount_paid"]) == 300.00


def test_delete_payment_success(authed_client, sale_with_total):
    created = authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "150.00"},
    ).json()
    response = authed_client.delete(f"/payments/{created['payment_id']}")
    assert response.status_code == 204
    response = authed_client.get(f"/payments/{created['payment_id']}")
    assert response.status_code == 404


def test_list_payments_for_sale(authed_client, sale_with_total):
    authed_client.post(
        "/payments/",
        json={"sale_id": sale_with_total, "payment_method": "cash", "amount_paid": "100.00"},
    )
    response = authed_client.get(f"/payments/by-sale/{sale_with_total}")
    assert response.status_code == 200
    assert len(response.json()) == 1


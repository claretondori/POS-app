import pytest


@pytest.fixture
def sale_setup(authed_client):
    """Creates a cashier, a stocked product, and an open sale to hang
    sale-item tests off of. Uses `authed_client` because creating the
    product goes through the protected /products endpoint."""
    user_id = authed_client.post(
        "/users/",
        json={"username": "item_cashier", "full_name": "Item Cashier", "password": "itempass123"},
    ).json()["user_id"]
    category_id = authed_client.post("/categories/", json={"name": "Stationery"}).json()["category_id"]
    product = authed_client.post(
        "/products/",
        json={
            "sku": "PEN-001",
            "name": "Blue Pen",
            "category_id": category_id,
            "unit_price": "20.00",
            "cost_price": "10.00",
            "quantity_in_stock": 10,
        },
    ).json()
    sale = authed_client.post("/sales/", json={"user_id": user_id}).json()
    return {"user_id": user_id, "product": product, "sale": sale}


def test_create_sale_item_success_updates_stock_and_sale_total(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    sale_id = sale_setup["sale"]["sale_id"]

    response = authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 3},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["quantity"] == 3
    assert float(body["subtotal"]) == 60.00

    product_response = authed_client.get(f"/products/{product_id}")
    assert product_response.json()["quantity_in_stock"] == 7

    sale_response = authed_client.get(f"/sales/{sale_id}")
    assert float(sale_response.json()["total_amount"]) == 60.00


def test_create_sale_item_insufficient_stock_returns_400(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    sale_id = sale_setup["sale"]["sale_id"]

    response = authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 999},
    )
    assert response.status_code == 400


def test_create_sale_item_nonexistent_sale_returns_400(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    response = authed_client.post(
        "/sale-items/",
        json={"sale_id": 999, "product_id": product_id, "quantity": 1},
    )
    assert response.status_code == 400


def test_create_sale_item_nonexistent_product_returns_400(authed_client, sale_setup):
    sale_id = sale_setup["sale"]["sale_id"]
    response = authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": 999, "quantity": 1},
    )
    assert response.status_code == 400


def test_create_sale_item_zero_quantity_returns_422(authed_client, sale_setup):
    response = authed_client.post(
        "/sale-items/",
        json={
            "sale_id": sale_setup["sale"]["sale_id"],
            "product_id": sale_setup["product"]["product_id"],
            "quantity": 0,
        },
    )
    assert response.status_code == 422


def test_update_sale_item_quantity_adjusts_stock_and_total(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    sale_id = sale_setup["sale"]["sale_id"]
    item = authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 2},
    ).json()

    response = authed_client.put(
        f"/sale-items/{item['sale_item_id']}",
        json={"quantity": 5},
    )
    assert response.status_code == 200
    assert float(response.json()["subtotal"]) == 100.00

    product_response = authed_client.get(f"/products/{product_id}")
    assert product_response.json()["quantity_in_stock"] == 5  # 10 - 5


def test_delete_sale_item_restocks_product_and_reduces_sale_total(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    sale_id = sale_setup["sale"]["sale_id"]
    item = authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 4},
    ).json()

    response = authed_client.delete(f"/sale-items/{item['sale_item_id']}")
    assert response.status_code == 204

    product_response = authed_client.get(f"/products/{product_id}")
    assert product_response.json()["quantity_in_stock"] == 10

    sale_response = authed_client.get(f"/sales/{sale_id}")
    assert float(sale_response.json()["total_amount"]) == 0


def test_get_sale_item_not_found_returns_404(authed_client):
    response = authed_client.get("/sale-items/999")
    assert response.status_code == 404


def test_list_sale_items_for_sale(authed_client, sale_setup):
    product_id = sale_setup["product"]["product_id"]
    sale_id = sale_setup["sale"]["sale_id"]
    authed_client.post(
        "/sale-items/",
        json={"sale_id": sale_id, "product_id": product_id, "quantity": 1},
    )
    response = authed_client.get(f"/sale-items/by-sale/{sale_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1


import pytest


@pytest.fixture
def category_id(authed_client):
    response = authed_client.post("/categories/", json={"name": "Soft Drinks"})
    return response.json()["category_id"]


def test_create_product_success(authed_client, category_id):
    response = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-001",
            "name": "Coca-Cola 500ml",
            "category_id": category_id,
            "unit_price": "80.00",
            "cost_price": "55.00",
            "quantity_in_stock": 100,
            "reorder_level": 10,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["sku"] == "SKU-001"
    assert body["quantity_in_stock"] == 100


def test_create_product_missing_required_field_returns_422(authed_client, category_id):
    response = authed_client.post(
        "/products/",
        json={
            "name": "Fanta 500ml",
            "category_id": category_id,
            "unit_price": "80.00",
            "cost_price": "55.00",
        },
    )
    assert response.status_code == 422


def test_create_product_duplicate_sku_returns_400(authed_client, category_id):
    payload = {
        "sku": "SKU-002",
        "name": "Sprite 500ml",
        "category_id": category_id,
        "unit_price": "80.00",
        "cost_price": "55.00",
    }
    authed_client.post("/products/", json=payload)
    response = authed_client.post("/products/", json=payload)
    assert response.status_code == 400


def test_create_product_nonexistent_category_returns_400(authed_client):
    response = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-003",
            "name": "Water 1L",
            "category_id": 999,
            "unit_price": "50.00",
            "cost_price": "30.00",
        },
    )
    assert response.status_code == 400


def test_create_product_nonexistent_supplier_returns_400(authed_client, category_id):
    response = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-004",
            "name": "Juice 1L",
            "category_id": category_id,
            "supplier_id": 999,
            "unit_price": "120.00",
            "cost_price": "90.00",
        },
    )
    assert response.status_code == 400


def test_get_product_not_found_returns_404(authed_client):
    response = authed_client.get("/products/999")
    assert response.status_code == 404


def test_update_product_success(authed_client, category_id):
    created = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-005",
            "name": "Milk 500ml",
            "category_id": category_id,
            "unit_price": "60.00",
            "cost_price": "40.00",
        },
    ).json()
    response = authed_client.put(
        f"/products/{created['product_id']}",
        json={"unit_price": "65.00"},
    )
    assert response.status_code == 200
    assert float(response.json()["unit_price"]) == 65.00


def test_update_product_nonexistent_category_returns_400(authed_client, category_id):
    created = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-006",
            "name": "Bread",
            "category_id": category_id,
            "unit_price": "70.00",
            "cost_price": "50.00",
        },
    ).json()
    response = authed_client.put(
        f"/products/{created['product_id']}",
        json={"category_id": 999},
    )
    assert response.status_code == 400


def test_delete_product_success(authed_client, category_id):
    created = authed_client.post(
        "/products/",
        json={
            "sku": "SKU-007",
            "name": "Eggs Tray",
            "category_id": category_id,
            "unit_price": "350.00",
            "cost_price": "300.00",
        },
    ).json()
    response = authed_client.delete(f"/products/{created['product_id']}")
    assert response.status_code == 204
    response = authed_client.get(f"/products/{created['product_id']}")
    assert response.status_code == 404


def test_list_products_returns_all_created(authed_client, category_id):
    authed_client.post(
        "/products/",
        json={
            "sku": "SKU-008",
            "name": "Rice 2kg",
            "category_id": category_id,
            "unit_price": "250.00",
            "cost_price": "200.00",
        },
    )
    response = authed_client.get("/products/")
    assert response.status_code == 200
    assert any(p["sku"] == "SKU-008" for p in response.json())


def test_low_stock_products_only_returns_products_at_or_below_reorder_level(authed_client, category_id):
    authed_client.post(
        "/products/",
        json={
            "sku": "SKU-009",
            "name": "Sugar 1kg",
            "category_id": category_id,
            "unit_price": "150.00",
            "cost_price": "120.00",
            "quantity_in_stock": 2,
            "reorder_level": 5,
        },
    )
    authed_client.post(
        "/products/",
        json={
            "sku": "SKU-010",
            "name": "Flour 2kg",
            "category_id": category_id,
            "unit_price": "180.00",
            "cost_price": "140.00",
            "quantity_in_stock": 50,
            "reorder_level": 5,
        },
    )
    response = authed_client.get("/products/low-stock")
    assert response.status_code == 200
    skus = [p["sku"] for p in response.json()]
    assert "SKU-009" in skus
    assert "SKU-010" not in skus


def test_list_products_without_credentials_returns_401(client):
    response = client.get("/products/")
    assert response.status_code == 401


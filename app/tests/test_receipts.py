import pytest


@pytest.fixture
def sale_and_user(authed_client):
    user_id = authed_client.post(
        "/users/",
        json={"username": "receipt_cashier", "full_name": "Receipt Cashier", "password": "receiptpass1"},
    ).json()["user_id"]
    sale_id = authed_client.post("/sales/", json={"user_id": user_id}).json()["sale_id"]
    return {"user_id": user_id, "sale_id": sale_id}


def test_create_receipt_success(authed_client, sale_and_user):
    response = authed_client.post(
        "/receipts/",
        json={"sale_id": sale_and_user["sale_id"], "issued_by": sale_and_user["user_id"]},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["sale_id"] == sale_and_user["sale_id"]
    assert body["receipt_number"].startswith("RCPT-")


def test_create_receipt_duplicate_for_sale_returns_400(authed_client, sale_and_user):
    payload = {"sale_id": sale_and_user["sale_id"], "issued_by": sale_and_user["user_id"]}
    authed_client.post("/receipts/", json=payload)
    response = authed_client.post("/receipts/", json=payload)
    assert response.status_code == 400


def test_create_receipt_nonexistent_sale_returns_400(authed_client, sale_and_user):
    response = authed_client.post(
        "/receipts/",
        json={"sale_id": 999, "issued_by": sale_and_user["user_id"]},
    )
    assert response.status_code == 400


def test_create_receipt_nonexistent_issuer_returns_400(authed_client, sale_and_user):
    response = authed_client.post(
        "/receipts/",
        json={"sale_id": sale_and_user["sale_id"], "issued_by": 999},
    )
    assert response.status_code == 400


def test_get_receipt_not_found_returns_404(authed_client):
    response = authed_client.get("/receipts/999")
    assert response.status_code == 404


def test_get_receipt_for_sale_not_found_returns_404(authed_client, sale_and_user):
    response = authed_client.get(f"/receipts/by-sale/{sale_and_user['sale_id']}")
    assert response.status_code == 404


def test_get_receipt_for_sale_success(authed_client, sale_and_user):
    authed_client.post(
        "/receipts/",
        json={"sale_id": sale_and_user["sale_id"], "issued_by": sale_and_user["user_id"]},
    )
    response = authed_client.get(f"/receipts/by-sale/{sale_and_user['sale_id']}")
    assert response.status_code == 200


def test_delete_receipt_success(authed_client, sale_and_user):
    created = authed_client.post(
        "/receipts/",
        json={"sale_id": sale_and_user["sale_id"], "issued_by": sale_and_user["user_id"]},
    ).json()
    response = authed_client.delete(f"/receipts/{created['receipt_id']}")
    assert response.status_code == 204
    response = authed_client.get(f"/receipts/{created['receipt_id']}")
    assert response.status_code == 404


def test_list_receipts_returns_all_created(authed_client, sale_and_user):
    authed_client.post(
        "/receipts/",
        json={"sale_id": sale_and_user["sale_id"], "issued_by": sale_and_user["user_id"]},
    )
    response = authed_client.get("/receipts/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


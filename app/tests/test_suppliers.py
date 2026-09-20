def test_create_supplier_success(client):
    response = client.post(
        "/suppliers/",
        json={"name": "Nairobi Wholesalers", "phone": "0733445566", "contact_person": "Peter Kiptoo"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Nairobi Wholesalers"


def test_create_supplier_missing_phone_returns_422(client):
    response = client.post("/suppliers/", json={"name": "Mombasa Traders"})
    assert response.status_code == 422


def test_get_supplier_not_found_returns_404(client):
    response = client.get("/suppliers/999")
    assert response.status_code == 404


def test_update_supplier_success(client):
    created = client.post(
        "/suppliers/", json={"name": "Kisumu Distributors", "phone": "0711000000"}
    ).json()
    response = client.put(
        f"/suppliers/{created['supplier_id']}",
        json={"contact_person": "Grace Otieno"},
    )
    assert response.status_code == 200
    assert response.json()["contact_person"] == "Grace Otieno"


def test_delete_supplier_success(client):
    created = client.post(
        "/suppliers/", json={"name": "Eldoret Supplies", "phone": "0722000000"}
    ).json()
    response = client.delete(f"/suppliers/{created['supplier_id']}")
    assert response.status_code == 204
    response = client.get(f"/suppliers/{created['supplier_id']}")
    assert response.status_code == 404


def test_list_suppliers_returns_all_created(client):
    client.post("/suppliers/", json={"name": "Thika Traders", "phone": "0700111222"})
    response = client.get("/suppliers/")
    assert response.status_code == 200
    assert any(s["name"] == "Thika Traders" for s in response.json())


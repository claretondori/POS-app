def test_create_category_success(client):
    response = client.post(
        "/categories/",
        json={"name": "Beverages", "description": "Cold and hot drinks"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Beverages"
    assert body["description"] == "Cold and hot drinks"
    assert "category_id" in body


def test_create_category_missing_name_returns_422(client):
    response = client.post("/categories/", json={"description": "No name given"})
    assert response.status_code == 422


def test_create_category_duplicate_name_returns_400(client):
    client.post("/categories/", json={"name": "Snacks"})
    response = client.post("/categories/", json={"name": "Snacks"})
    assert response.status_code == 400


def test_get_category_success(client):
    created = client.post("/categories/", json={"name": "Dairy"}).json()
    response = client.get(f"/categories/{created['category_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Dairy"


def test_get_category_not_found_returns_404(client):
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_list_categories_returns_all_created(client):
    client.post("/categories/", json={"name": "Bakery"})
    client.post("/categories/", json={"name": "Produce"})
    response = client.get("/categories/")
    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert "Bakery" in names
    assert "Produce" in names


def test_update_category_success(client):
    created = client.post("/categories/", json={"name": "Frozen"}).json()
    response = client.put(
        f"/categories/{created['category_id']}",
        json={"description": "Frozen goods"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Frozen goods"
    assert response.json()["name"] == "Frozen"


def test_update_category_not_found_returns_404(client):
    response = client.put("/categories/999", json={"name": "Nope"})
    assert response.status_code == 404


def test_delete_category_success(client):
    created = client.post("/categories/", json={"name": "Cleaning"}).json()
    response = client.delete(f"/categories/{created['category_id']}")
    assert response.status_code == 204
    response = client.get(f"/categories/{created['category_id']}")
    assert response.status_code == 404


def test_delete_category_not_found_returns_404(client):
    response = client.delete("/categories/999")
    assert response.status_code == 404


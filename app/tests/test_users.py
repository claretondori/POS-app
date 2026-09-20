def test_create_user_success(client):
    response = client.post(
        "/users/",
        json={
            "username": "cashier1",
            "full_name": "Grace Wambui",
            "password": "supersecret1",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "cashier1"
    assert body["role"] == "cashier"
    assert "password" not in body
    assert "password_hash" not in body


def test_create_user_duplicate_username_returns_400(client):
    payload = {"username": "manager1", "full_name": "Peter Njogu", "password": "managerpass1"}
    client.post("/users/", json=payload)
    response = client.post("/users/", json=payload)
    assert response.status_code == 400


def test_create_user_short_password_returns_422(client):
    response = client.post(
        "/users/",
        json={"username": "shortpw", "full_name": "Test User", "password": "short"},
    )
    assert response.status_code == 422


def test_get_user_not_found_returns_404(client):
    response = client.get("/users/999")
    assert response.status_code == 404


def test_update_user_success(client):
    created = client.post(
        "/users/",
        json={"username": "updateuser", "full_name": "Old Name", "password": "originalpass1"},
    ).json()
    response = client.put(
        f"/users/{created['user_id']}",
        json={"full_name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "New Name"


def test_delete_user_success(client):
    created = client.post(
        "/users/",
        json={"username": "deleteuser", "full_name": "Delete Me", "password": "deletepass1"},
    ).json()
    response = client.delete(f"/users/{created['user_id']}")
    assert response.status_code == 204
    response = client.get(f"/users/{created['user_id']}")
    assert response.status_code == 404


def test_list_users_returns_all_created(client):
    client.post(
        "/users/",
        json={"username": "listeduser", "full_name": "Listed User", "password": "listedpass1"},
    )
    response = client.get("/users/")
    assert response.status_code == 200
    assert any(u["username"] == "listeduser" for u in response.json())


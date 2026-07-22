from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_item_returns_created_item():
    response = client.post("/items", json={"name": "Widget", "price": 9.99})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Widget"
    assert body["price"] == 9.99
    assert "id" in body


def test_get_item_returns_previously_created_item():
    create_response = client.post("/items", json={"name": "Gadget", "price": 19.99})
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == item_id
    assert body["name"] == "Gadget"
    assert body["price"] == 19.99


def test_get_item_returns_404_when_item_does_not_exist():
    response = client.get("/items/does-not-exist")

    assert response.status_code == 404


def test_create_item_rejects_missing_name():
    response = client.post("/items", json={"price": 9.99})

    assert response.status_code == 422

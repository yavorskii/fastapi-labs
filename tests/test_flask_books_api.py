import pytest

from app.main_flask import app as flask_app


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    return flask_app.test_client()


def test_create_get_list_delete_flow(client):
    create = client.post(
        "/books",
        json={"title": "Clean Code", "author": "Robert Martin", "year": 2008, "status": "наявна", "description": None},
    )
    assert create.status_code == 201
    book_id = create.get_json()["id"]

    get_res = client.get(f"/books/{book_id}")
    assert get_res.status_code == 200
    assert get_res.get_json()["title"] == "Clean Code"

    list_res = client.get("/books?limit=10&offset=0")
    assert list_res.status_code == 200
    data = list_res.get_json()
    assert data["total"] == 1
    assert data["limit"] == 10
    assert data["offset"] == 0
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == book_id

    delete = client.delete(f"/books/{book_id}")
    assert delete.status_code == 204

    missing = client.get(f"/books/{book_id}")
    assert missing.status_code == 404
    assert missing.get_json()["message"] == "Book not found"


def test_list_filters_and_paginates(client):
    client.post("/books", json={"title": "A", "author": "Kent Beck", "year": 2002, "status": "наявна"})
    client.post("/books", json={"title": "B", "author": "Martin Fowler", "year": 1999, "status": "наявна"})
    client.post("/books", json={"title": "C", "author": "Robert Martin", "year": 2008, "status": "видана"})

    res = client.get("/books?limit=1&offset=0&status=наявна&author=fowler")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "B"


def test_invalid_id_returns_404(client):
    res = client.get("/books/not-an-objectid")
    assert res.status_code == 404
    assert res.get_json()["message"] == "Book not found"

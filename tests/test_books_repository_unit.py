import pytest
from bson import ObjectId

from app.repository.mongo_repo import MongoBookRepository


def test_repo_add_and_get_by_id(fake_db):
    repo = MongoBookRepository(fake_db)
    created = repo.add(fake_db, {"title": "A", "author": "X", "year": 2000, "status": "наявна", "description": None})
    assert ObjectId.is_valid(created["id"])

    loaded = repo.get_by_id(fake_db, created["id"])
    assert loaded["title"] == "A"


def test_repo_get_all_maps_id(fake_db):
    repo = MongoBookRepository(fake_db)
    repo.add(fake_db, {"title": "A", "author": "X", "year": 2000, "status": "наявна", "description": None})
    items = repo.get_all(fake_db, limit=10, offset=0, status=None, author=None)
    assert len(items) == 1
    assert "id" in items[0]
    assert "_id" not in items[0]


def test_repo_delete_invalid_id_returns_false(fake_db):
    repo = MongoBookRepository(fake_db)
    assert repo.delete(fake_db, "not-an-objectid") is False

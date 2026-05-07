import pytest

from app.services.book_service import BookService


def test_build_query_empty():
    service = BookService()
    assert service._build_query() == {}


def test_build_query_with_status_and_author():
    service = BookService()
    q = service._build_query(status="наявна", author="martin")
    assert q["status"] == "наявна"
    assert q["author"]["$regex"] == "martin"
    assert "i" in q["author"]["$options"]


@pytest.mark.anyio
async def test_get_books_returns_envelope(monkeypatch, fake_db):
    service = BookService()

    async def _get_all(self, db, limit, offset, status, author):
        return [{"id": "1", "title": "A", "author": "X", "year": 2000, "status": "наявна", "description": None}]

    repo_instance = type("Repo", (), {"get_all": _get_all})()
    monkeypatch.setattr(service, "repo", lambda _db: repo_instance)

    async def _count_documents(_query):
        return 1

    fake_db.books.count_documents = _count_documents

    res = await service.get_books(fake_db, limit=10, offset=0, status=None, author=None)
    assert res["total"] == 1
    assert res["limit"] == 10
    assert res["offset"] == 0
    assert len(res["items"]) == 1

import pytest
from types import SimpleNamespace
from httpx import AsyncClient

from backend.main import app


@pytest.mark.asyncio
async def test_create_serial(monkeypatch):
    payload = {"slug": "s1", "name": "S1", "description": "desc", "rating": 8.5, "category": "drama"}

    async def fake_create(**data):
        return SimpleNamespace(
            id=1,
            slug=data["slug"],
            name=data["name"],
            description=data.get("description"),
            rating=data.get("rating"),
            category=data.get("category"),
            seasons=[],
            created_at=None,
            updated_at=None,
        )

    monkeypatch.setattr("app.serials.dao.SerialDAO.create", fake_create)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/serials/", json=payload)

    assert r.status_code == 201
    assert r.json()["slug"] == "s1"


@pytest.mark.asyncio
async def test_get_serial_with_relations(monkeypatch):
    chapter = SimpleNamespace(id=10, number=1, name="Ch1", description="c", created_at=None, updated_at=None)
    season = SimpleNamespace(id=2, number=1, name="S1", description=None, chapters=[chapter], created_at=None, updated_at=None)
    serial = SimpleNamespace(id=1, slug="s1", name="S1", description=None, rating=8.0, category="drama", seasons=[season], created_at=None, updated_at=None)

    async def fake_find(**filters):
        return serial

    monkeypatch.setattr("app.serials.dao.SerialDAO.find_one_with_relations", fake_find)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/serials/s1")

    assert r.status_code == 200
    data = r.json()
    assert data["slug"] == "s1"
    assert isinstance(data.get("seasons"), list)
    assert data["seasons"][0]["chapters"][0]["number"] == 1


@pytest.mark.asyncio
async def test_add_chapter_comment(monkeypatch):
    chapter = SimpleNamespace(id=10, number=1, name="Ch1", description="c", created_at=None, updated_at=None)
    season = SimpleNamespace(id=2, number=1, name="S1", description=None, chapters=[chapter], created_at=None, updated_at=None)
    serial = SimpleNamespace(id=1, slug="s1", name="S1", description=None, rating=8.0, category="drama", seasons=[season], created_at=None, updated_at=None)

    async def fake_find(**filters):
        return serial

    async def fake_create(**data):
        return SimpleNamespace(
            id=123,
            user_id=data.get("user_id"),
            text=data.get("text"),
            parent_id=None,
            content_type=2,
            content_id=data.get("content_id") or 10,
            created_at=None,
            updated_at=None,
        )

    monkeypatch.setattr("app.serials.dao.SerialDAO.find_one_with_relations", fake_find)
    monkeypatch.setattr("app.comments.dao.CommentDAO.create", fake_create)
    # auth dependency returns user with id=1
    monkeypatch.setattr("app.api.deps.get_current_user", lambda: SimpleNamespace(id=1))

    payload = {"user_id": 1, "text": "Nice chapter"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/api/v1/serials/s1/seasons/1/chapters/1/comments", json=payload)

    assert r.status_code == 201


@pytest.mark.asyncio
async def test_update_comment(monkeypatch):
    async def fake_get(obj_id):
        return SimpleNamespace(id=obj_id, user_id=1, text="old")

    async def fake_update(obj_id=None, **data):
        return {"id": obj_id, "text": data.get("text"), "user_id": 1}

    monkeypatch.setattr("app.comments.dao.CommentDAO.get", fake_get)
    monkeypatch.setattr("app.comments.dao.CommentDAO.update", fake_update)
    monkeypatch.setattr("app.api.deps.get_current_user", lambda: SimpleNamespace(id=1))

    payload = {"text": "updated"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.put("/api/v1/comments/5", json=payload)

    assert r.status_code == 200
    assert r.json()["text"] == "updated"


@pytest.mark.asyncio
async def test_delete_comment(monkeypatch):
    async def fake_get(obj_id):
        return SimpleNamespace(id=obj_id, user_id=1, text="old")

    async def fake_delete(obj_id=None, **filters):
        return True

    monkeypatch.setattr("app.comments.dao.CommentDAO.get", fake_get)
    monkeypatch.setattr("app.comments.dao.CommentDAO.delete", fake_delete)
    monkeypatch.setattr("app.api.deps.get_current_user", lambda: SimpleNamespace(id=1))

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.delete("/api/v1/comments/5")

    assert r.status_code == 204

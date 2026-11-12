import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.main import app, get_repo
from tests.fakes import InMemoryRepo


class BrokenRepo(InMemoryRepo):
    def ping(self) -> None:
        raise SQLAlchemyError("baza nije dostupna")


@pytest.fixture
def client():
    repo = InMemoryRepo()
    app.dependency_overrides[get_repo] = lambda: repo
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_ready(client):
    assert client.get("/ready").json() == {"status": "ready"}


def test_nije_spremna_bez_baze():
    app.dependency_overrides[get_repo] = lambda: BrokenRepo()
    try:
        assert TestClient(app).get("/ready").status_code == 503
    finally:
        app.dependency_overrides.clear()


def test_nova_beleska(client):
    r = client.post("/notes", json={"title": "  DevOps  ", "body": "uvod"})
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "DevOps", "body": "uvod"}


def test_lista_i_pretraga(client):
    client.post("/notes", json={"title": "DevOps"})
    client.post("/notes", json={"title": "Docker"})
    assert len(client.get("/notes").json()) == 2
    nadjene = client.get("/notes", params={"q": "dev"}).json()
    assert [n["title"] for n in nadjene] == ["DevOps"]


def test_prazan_naslov_je_greska(client):
    assert client.post("/notes", json={"title": "   "}).status_code == 422


def test_brisanje(client):
    note_id = client.post("/notes", json={"title": "DevOps"}).json()["id"]
    assert client.delete(f"/notes/{note_id}").status_code == 204
    assert client.get("/notes").json() == []


def test_brisanje_nepostojece(client):
    assert client.delete("/notes/999").status_code == 404

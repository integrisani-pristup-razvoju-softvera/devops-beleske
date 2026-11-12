"""REST API aplikacije Beleške."""

import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy.exc import SQLAlchemyError

from app.db import Base, NoteRepository, get_engine
from app.notes import normalize_title

log = logging.getLogger("beleske")


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Tabele se prave pri pokretanju; ako baza još nije dostupna, aplikacija ipak
    # startuje (/health radi), a /ready javlja da nije spremna.
    try:
        Base.metadata.create_all(get_engine())
    except SQLAlchemyError as exc:
        log.warning("baza nije dostupna pri pokretanju: %s", exc)
    yield


app = FastAPI(title="Beleške", version="0.1.0", lifespan=lifespan)


def get_repo() -> NoteRepository:
    return NoteRepository(get_engine())


Repo = Annotated[NoteRepository, Depends(get_repo)]


class NoteIn(BaseModel):
    title: str
    body: str = ""

    @field_validator("title")
    @classmethod
    def title_ok(cls, value: str) -> str:
        return normalize_title(value)


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    body: str


@app.get("/health")
def health():
    """Proces radi (liveness)."""
    return {"status": "ok"}


@app.get("/ready")
def ready(repo: Repo):
    """Proces radi i baza je dostupna (readiness)."""
    try:
        repo.ping()
    except SQLAlchemyError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "baza nije dostupna") from exc
    return {"status": "ready"}


@app.get("/notes", response_model=list[NoteOut])
def list_notes(repo: Repo, q: str | None = None):
    return repo.list(q)


@app.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteIn, repo: Repo):
    return repo.create(title=note.title, body=note.body)


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, repo: Repo):
    if not repo.delete(note_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "beleška ne postoji")

"""Pristup bazi: model beleške i repozitorijum.

Adresa baze se čita iz promenljive okruženja DATABASE_URL (Twelve-Factor, faktor III).
"""

import os
from datetime import UTC, datetime
from functools import lru_cache

from sqlalchemy import DateTime, Engine, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:dev@localhost:5432/postgres"


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


class NoteRepository:
    """Čuva beleške u relacionoj bazi (PostgreSQL u radu, bilo koja baza u testovima)."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, title: str, body: str = "") -> Note:
        with Session(self.engine, expire_on_commit=False) as session:
            note = Note(title=title, body=body)
            session.add(note)
            session.commit()
            return note

    def list(self, q: str | None = None) -> list[Note]:
        stmt = select(Note).order_by(Note.id)
        if q:
            stmt = stmt.where(Note.title.ilike(f"%{q}%"))
        with Session(self.engine) as session:
            return list(session.scalars(stmt))

    def delete(self, note_id: int) -> bool:
        with Session(self.engine) as session:
            note = session.get(Note, note_id)
            if note is None:
                return False
            session.delete(note)
            session.commit()
            return True

    def ping(self) -> None:
        """Baca izuzetak ako baza nije dostupna."""
        with self.engine.connect() as conn:
            conn.execute(select(1))


@lru_cache
def get_engine() -> Engine:
    return create_engine(os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL), pool_pre_ping=True)

"""Repozitorijum u memoriji: test dvojnik za NoteRepository u jediničnim testovima."""

from dataclasses import dataclass, field
from itertools import count


@dataclass
class FakeNote:
    id: int
    title: str
    body: str = ""


@dataclass
class InMemoryRepo:
    """Isti interfejs kao app.db.NoteRepository, bez baze."""

    notes: dict[int, FakeNote] = field(default_factory=dict)
    ids: count = field(default_factory=lambda: count(1))

    def create(self, title: str, body: str = "") -> FakeNote:
        note = FakeNote(next(self.ids), title, body)
        self.notes[note.id] = note
        return note

    def list(self, q: str | None = None) -> list[FakeNote]:
        found = self.notes.values()
        if q:
            found = [n for n in found if q.lower() in n.title.lower()]
        return sorted(found, key=lambda n: n.id)

    def delete(self, note_id: int) -> bool:
        return self.notes.pop(note_id, None) is not None

    def ping(self) -> None:
        return None

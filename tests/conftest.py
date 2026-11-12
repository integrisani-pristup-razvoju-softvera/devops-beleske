import os

import pytest
from sqlalchemy import create_engine

from app.db import Base, NoteRepository


@pytest.fixture
def repo():
    """Repozitorijum nad pravom bazom; svaki test počinje od prazne baze."""
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("nema TEST_DATABASE_URL")
    eng = create_engine(url)
    Base.metadata.create_all(eng)
    yield NoteRepository(eng)
    Base.metadata.drop_all(eng)
    eng.dispose()

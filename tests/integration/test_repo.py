import pytest


@pytest.mark.integration
def test_upis_i_citanje(repo):
    repo.create(title="DevOps")
    assert len(repo.list()) == 1


@pytest.mark.integration
def test_pretraga_ne_razlikuje_velika_slova(repo):
    repo.create(title="DevOps")
    repo.create(title="Docker")
    assert [n.title for n in repo.list("DEV")] == ["DevOps"]


@pytest.mark.integration
def test_brisanje(repo):
    note = repo.create(title="DevOps")
    assert repo.delete(note.id)
    assert not repo.delete(note.id)
    assert repo.list() == []

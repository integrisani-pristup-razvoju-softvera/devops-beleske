import pytest

from app.notes import normalize_title


@pytest.mark.parametrize(
    "ulaz, ocekivano",
    [
        ("  DevOps ", "DevOps"),
        ("a" * 150, "a" * 100),
    ],
)
def test_normalizacija(ulaz, ocekivano):
    assert normalize_title(ulaz) == ocekivano


def test_prazan_naslov():
    with pytest.raises(ValueError):
        normalize_title("   ")

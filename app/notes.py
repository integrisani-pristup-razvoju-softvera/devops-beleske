"""Pravila za beleške koja ne zavise ni od baze ni od HTTP-a."""

MAX_TITLE = 100


def normalize_title(title: str) -> str:
    """Skida razmake sa krajeva i skraćuje naslov na MAX_TITLE znakova."""
    title = title.strip()
    if not title:
        raise ValueError("prazan naslov")
    return title[:MAX_TITLE]

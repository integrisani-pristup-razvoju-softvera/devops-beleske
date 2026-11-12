# Beleške — primer-aplikacija

Mala REST aplikacija (Python 3.12, FastAPI, PostgreSQL) za auditivne i laboratorijske vežbe predmeta
**Integrisani pristup razvoju softvera** (Elektronski fakultet u Nišu). Aplikacija je namerno
jednostavna: težište predmeta je na njenoj isporuci, ne na razvoju.

## Endpoint-i

| Metod  | Putanja        | Šta radi                                  |
|--------|----------------|-------------------------------------------|
| GET    | `/health`      | proces radi (liveness)                    |
| GET    | `/ready`       | proces radi i baza je dostupna (readiness)|
| GET    | `/notes?q=…`   | lista beležaka, opciono pretraga po naslovu |
| POST   | `/notes`       | nova beleška: `{"title": "…", "body": "…"}` |
| DELETE | `/notes/{id}`  | brisanje beleške                          |

Interaktivna dokumentacija API-ja je na `http://localhost:8000/docs`.

## Pokretanje (WSL2 ili Linux)

```bash
python3 -m venv .venv && source .venv/bin/activate
make install          # zavisnosti za rad i za razvoj
make db               # PostgreSQL 16 u Docker-u, port 5432
make run              # http://localhost:8000
curl localhost:8000/health
```

## Testovi i provere

```bash
make test-unit        # samo jedinični testovi, bez baze
make test             # svi testovi; integracioni se preskaču ako nema TEST_DATABASE_URL
make lint             # ruff check i provera formatiranja
make format           # ispravlja formatiranje i ono što ruff ume sam
make check            # lint + test: isto što radi CI
```

Integracioni testovi sa pravom bazom:

```bash
make test-db          # PostgreSQL 16 u Docker-u, port 5433
export TEST_DATABASE_URL=postgresql+psycopg://postgres:test@localhost:5433/postgres
make test
```

## Konfiguracija

Aplikacija čita konfiguraciju iz promenljivih okruženja (Twelve-Factor, faktor III).
Primer je u `.env.example`; kopirajte ga u `.env`, koji nikad ne ide u Git.

| Promenljiva         | Značenje                       | Podrazumevano                                              |
|---------------------|--------------------------------|------------------------------------------------------------|
| `DATABASE_URL`      | baza aplikacije                | `postgresql+psycopg://postgres:dev@localhost:5432/postgres` |
| `TEST_DATABASE_URL` | baza za integracione testove   | nema (integracioni testovi se preskaču)                    |

## Struktura

```
app/
  main.py            # rute i zavisnosti (get_repo)
  db.py              # model Note i NoteRepository
  notes.py           # pravila koja ne zavise od baze (normalize_title)
tests/
  conftest.py        # fixture repo nad pravom bazom
  fakes.py           # InMemoryRepo, test dvojnik za jedinične testove
  unit/              # brzi testovi, bez baze
  integration/       # testovi sa pravom bazom (marker integration)
Makefile
pyproject.toml       # podešavanja za pytest, coverage i ruff
requirements.txt     # zavisnosti aplikacije
requirements-dev.txt # alati za razvoj i testiranje
```

## Šta dodajete tokom semestra

| Vežba | Šta se dodaje u repozitorijum                                                   |
|-------|---------------------------------------------------------------------------------|
| L1    | nov endpoint (npr. `GET /notes/{id}` ili `PUT /notes/{id}`) sa testovima, `.pre-commit-config.yaml`, tag `v0.1.0` |
| L2    | `.github/workflows/ci.yml`, prag pokrivenosti (`fail_under`) u `pyproject.toml`, bedž u README-u |
| L3    | `Dockerfile`, `compose.yaml`, objava slike na GHCR                              |
| L4    | isporuka na staging i produkciju, bezbednosne provere u pipeline-u              |
| L5    | `infra/` (OpenTofu) i `ansible/`                                                |
| L6    | Kubernetes manifesti i Helm chart                                               |
| L7    | Argo CD, `/metrics`, dashboard i alarm                                          |

## Za nastavnika: objavljivanje šablona

Repozitorijum se objavljuje jednom, kao GitHub šablon; studenti prave svoj repozitorijum
dugmetom **Use this template**.

```bash
git init -b main
git add .
git commit -m "chore: početno stanje primer-aplikacije"
gh repo create IntegrisaniPristupRazvojuAplikacija/devops-beleske --public --source . --push
gh repo edit IntegrisaniPristupRazvojuAplikacija/devops-beleske --template
```

.PHONY: install run test-unit test lint format check db test-db

install:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	uvicorn app.main:app --reload --port 8000

test-unit:
	pytest tests/unit

test:
	pytest

lint:
	ruff check . && ruff format --check .

format:
	ruff format . && ruff check . --fix

check: lint test

# Razvojna baza na portu 5432 (DATABASE_URL iz .env.example)
db:
	docker run -d --name db -e POSTGRES_PASSWORD=dev -p 5432:5432 postgres:16

# Baza za integracione testove na portu 5433 (TEST_DATABASE_URL iz .env.example)
test-db:
	docker run -d --name testdb -e POSTGRES_PASSWORD=test -p 5433:5432 postgres:16

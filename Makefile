include .env
export

LOCAL_DB_URL = $(subst @db:,@localhost:,$(DATABASE_URL))

dev:
	poetry run uvicorn app.main:app --reload

test:
	poetry run pytest tests/ -v

lint:
	poetry run ruff check .

type-check:
	poetry run mypy

coverage:
	poetry run pytest tests/ --cov=app --cov-report=term-missing

# Docker
docker-up:
	docker compose up -d

db-shell:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)


docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-build:
	docker compose build

# Migrations (always run locally against localhost)
migrate:
	DATABASE_URL=$(LOCAL_DB_URL) poetry run alembic upgrade head

migrate-gen:
	DATABASE_URL=$(LOCAL_DB_URL) poetry run alembic revision --autogenerate -m "$(m)"

migrate-down:
	DATABASE_URL=$(LOCAL_DB_URL) poetry run alembic downgrade -1

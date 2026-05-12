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

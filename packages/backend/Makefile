.PHONY: help install dev test lint format clean migrate upgrade downgrade

help:
	@echo "MemoryVault Backend - Available commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make dev       - Run development server"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linters"
	@echo "  make format    - Format code"
	@echo "  make migrate   - Create new migration"
	@echo "  make upgrade   - Run migrations"
	@echo "  make downgrade - Rollback migration"
	@echo "  make clean     - Clean build artifacts"

install:
	pip install -r requirements/dev.txt

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v --cov=app --cov-report=html --cov-report=term

lint:
	mypy app/
	pylint app/
	black --check app/
	isort --check app/

format:
	black app/
	isort app/

migrate:
	alembic revision --autogenerate -m "$(msg)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov/ .mypy_cache/

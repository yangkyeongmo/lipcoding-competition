.PHONY: install run test lint clean dev

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Run the application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Run in development mode
dev:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Run tests
test:
	python -m pytest tests/ -v

# Lint code
lint:
	flake8 app/ --max-line-length=88 --extend-ignore=E203,W503
	black app/ --check
	isort app/ --check-only

# Format code
format:
	black app/
	isort app/

# Clean cache
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Initialize database
init-db:
	python -c "from app.database import init_db; init_db()"

# Setup project (install + init-db)
setup: install init-db

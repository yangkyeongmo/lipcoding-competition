.PHONY: install run test lint clean dev

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Run the application
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

# Run the application in background
run-bg:
	nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload > server.log 2>&1 & echo $$! > server.pid
	@echo "Backend server started in background (PID: $$(cat server.pid))"
	@echo "Logs: tail -f server.log"
	@echo "Stop: make stop"

# Stop background server
stop:
	@if [ -f server.pid ]; then \
		kill $$(cat server.pid) 2>/dev/null || true; \
		rm -f server.pid; \
		echo "Backend server stopped"; \
	else \
		echo "No server.pid file found"; \
	fi

# Check server status
status:
	@if [ -f server.pid ] && kill -0 $$(cat server.pid) 2>/dev/null; then \
		echo "Backend server is running (PID: $$(cat server.pid))"; \
	else \
		echo "Backend server is not running"; \
	fi

# View server logs
logs:
	@if [ -f server.log ]; then \
		tail -f server.log; \
	else \
		echo "No server.log file found"; \
	fi

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
	rm -f server.log server.pid nohup.out

# Initialize database
init-db:
	python -c "from app.database import init_db; init_db()"

# Setup project (install + init-db)
setup: install init-db

.PHONY: install run build test lint clean dev

# Install dependencies
install:
	npm install

# Run the application in development mode
run:
	npm start

# Run the application in background
run-bg:
	nohup npm start > frontend.log 2>&1 & echo $$! > frontend.pid
	@echo "Frontend server started in background (PID: $$(cat frontend.pid))"
	@echo "Logs: tail -f frontend.log"
	@echo "Stop: make stop"

# Stop background server
stop:
	@if [ -f frontend.pid ]; then \
		kill $$(cat frontend.pid) 2>/dev/null || true; \
		rm -f frontend.pid; \
		echo "Frontend server stopped"; \
	else \
		echo "No frontend.pid file found"; \
	fi

# Check server status
status:
	@if [ -f frontend.pid ] && kill -0 $$(cat frontend.pid) 2>/dev/null; then \
		echo "Frontend server is running (PID: $$(cat frontend.pid))"; \
	else \
		echo "Frontend server is not running"; \
	fi

# View server logs
logs:
	@if [ -f frontend.log ]; then \
		tail -f frontend.log; \
	else \
		echo "No frontend.log file found"; \
	fi

# Run in development mode
dev:
	npm start

# Build for production
build:
	npm run build

# Run tests
test:
	npm test

# Lint code
lint:
	npx eslint src/ --ext .js,.jsx,.ts,.tsx

# Format code
format:
	npx prettier --write src/

# Clean node_modules and reinstall
clean:
	rm -rf node_modules package-lock.json
	rm -f frontend.log frontend.pid nohup.out
	npm install

# Setup project (install dependencies)
setup: install

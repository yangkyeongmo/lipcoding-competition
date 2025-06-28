.PHONY: install test test-headed test-debug test-ui setup clean start-servers stop-servers status-servers logs-backend logs-frontend check-deps

# Check if dependencies are installed
check-deps:
	@echo "Checking dependencies..."
	@echo "=== Backend Dependencies ==="
	@cd backend && python -c "import fastapi, uvicorn, sqlalchemy" 2>/dev/null && echo "✓ Backend dependencies OK" || echo "✗ Backend dependencies missing - run: cd backend && make install"
	@echo "=== Frontend Dependencies ==="
	@cd frontend && [ -d node_modules ] && echo "✓ Frontend dependencies OK" || echo "✗ Frontend dependencies missing - run: cd frontend && make install"
	@echo "=== E2E Test Dependencies ==="
	@[ -d node_modules ] && echo "✓ E2E test dependencies OK" || echo "✗ E2E test dependencies missing - run: make install"

# Server management commands
start-servers:
	@echo "Starting backend server..."
	cd backend && make install && make run-bg
	@echo "Starting frontend server..."
	cd frontend && make install && make run-bg
	@echo "Both servers started in background"
	@echo "Backend: http://localhost:8080"
	@echo "Frontend: http://localhost:3000"

stop-servers:
	@echo "Stopping backend server..."
	cd backend && make stop
	@echo "Stopping frontend server..."
	cd frontend && make stop
	@echo "Both servers stopped"

status-servers:
	@echo "=== Backend Status ==="
	cd backend && make status
	@echo "=== Frontend Status ==="
	cd frontend && make status

logs-backend:
	cd backend && make logs

logs-frontend:
	cd frontend && make logs

# Install Playwright and dependencies
install:
	npm install
	npx playwright install

# Run all E2E tests
test:
	npx playwright test

# Run tests with browser UI (headed mode)
test-headed:
	npx playwright test --headed

# Run tests in debug mode
test-debug:
	npx playwright test --debug

# Run tests with Playwright UI
test-ui:
	npx playwright test --ui

# Run specific test file
test-auth:
	npx playwright test tests/auth.spec.js

test-api:
	npx playwright test tests/api.spec.js

test-mentor:
	npx playwright test tests/mentor.spec.js

test-mentee:
	npx playwright test tests/mentee.spec.js

test-ui-ux:
	npx playwright test tests/ui-ux.spec.js

test-integration:
	npx playwright test tests/integration.spec.js

# Setup test environment
setup: install
	@echo "Setting up E2E test environment..."
	@echo ""
	@echo "To start both servers in background:"
	@echo "  make start-servers"
	@echo ""
	@echo "Or start servers individually:"
	@echo "  Backend: cd backend && make run-bg"
	@echo "  Frontend: cd frontend && make run-bg"
	@echo ""
	@echo "Check server status:"
	@echo "  make status-servers"

# Generate test report
report:
	npx playwright show-report

# Clean up
clean:
	rm -rf test-results/
	rm -rf playwright-report/

# Run tests on specific browser
test-chrome:
	npx playwright test --project=chromium

test-firefox:
	npx playwright test --project=firefox

test-safari:
	npx playwright test --project=webkit

# Run tests in parallel
test-parallel:
	npx playwright test --workers=4

# Run tests with retries
test-retry:
	npx playwright test --retries=2

# Help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Server Management:"
	@echo "  check-deps    - Check if all dependencies are installed"
	@echo "  start-servers - Start both backend and frontend servers in background"
	@echo "  stop-servers  - Stop both servers"
	@echo "  status-servers - Check status of both servers"
	@echo "  logs-backend  - View backend server logs"
	@echo "  logs-frontend - View frontend server logs"
	@echo ""
	@echo "Testing:"
	@echo "  install       - Install Playwright and dependencies"
	@echo "  test          - Run all E2E tests"
	@echo "  test-headed   - Run tests with browser UI"
	@echo "  test-debug    - Run tests in debug mode"
	@echo "  test-ui       - Run tests with Playwright UI"
	@echo "  test-auth     - Run authentication tests"
	@echo "  test-api      - Run API integration tests"
	@echo "  test-mentor   - Run mentor feature tests"
	@echo "  test-mentee   - Run mentee feature tests"
	@echo "  test-ui-ux    - Run UI/UX tests"
	@echo "  test-integration - Run full integration tests"
	@echo ""
	@echo "Setup & Maintenance:"
	@echo "  setup         - Setup test environment"
	@echo "  report        - Show test report"
	@echo "  clean         - Clean test artifacts"
	@echo "  help          - Show this help message"

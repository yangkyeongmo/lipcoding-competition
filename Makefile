.PHONY: install test test-headed test-debug test-ui setup clean

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
	@echo "Make sure both backend and frontend servers are running:"
	@echo "Backend: cd backend && make run"
	@echo "Frontend: cd frontend && npm start"

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
	@echo "  setup         - Setup test environment"
	@echo "  report        - Show test report"
	@echo "  clean         - Clean test artifacts"
	@echo "  help          - Show this help message"

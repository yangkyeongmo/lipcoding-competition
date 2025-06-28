# E2E Testing for Mentor-Mentee Application

This directory contains comprehensive end-to-end (E2E) tests for the mentor-mentee application using Playwright.

## Test Coverage

### 🔐 Authentication Tests (`tests/auth.spec.js`)
- User registration (mentor and mentee)
- Login/logout functionality
- Form validation
- Error handling for invalid credentials
- Session management

### 👨‍🏫 Mentor Features (`tests/mentor.spec.js`)
- Mentor dashboard functionality
- Viewing and managing matching requests
- Accepting/rejecting mentorship requests
- Profile management
- Mentor-specific workflows

### 👨‍🎓 Mentee Features (`tests/mentee.spec.js`)
- Mentee dashboard functionality
- Browsing available mentors
- Sending matching requests
- Filtering mentors by expertise
- Profile management
- Request status tracking

### 🔗 API Integration (`tests/api.spec.js`)
- Backend API endpoint testing
- JWT token authentication
- CRUD operations for users and requests
- Error handling and validation
- Data consistency checks

### 🎨 UI/UX Tests (`tests/ui-ux.spec.js`)
- Responsive design testing
- Accessibility compliance
- Keyboard navigation
- Loading states
- Error message display
- Cross-browser compatibility

### 🔄 Integration Tests (`tests/integration.spec.js`)
- Complete user journeys
- Multi-user workflows
- Mentor-mentee matching process
- End-to-end scenarios

## Prerequisites

1. **Backend Server**: Make sure the FastAPI backend is running on `http://localhost:8080`
   ```bash
   cd backend && make run
   ```

2. **Frontend Server**: Make sure the React frontend is running on `http://localhost:3000`
   ```bash
   cd frontend && npm start
   ```

## Setup and Installation

1. Install dependencies:
   ```bash
   make install
   ```

2. Setup test environment:
   ```bash
   make setup
   ```

## Running Tests

### Quick Start
```bash
# Run all tests
make test

# Run tests with browser UI (to see what's happening)
make test-headed

# Run tests with Playwright UI (interactive)
make test-ui
```

### Specific Test Suites
```bash
# Authentication tests
make test-auth

# API integration tests
make test-api

# Mentor functionality tests
make test-mentor

# Mentee functionality tests
make test-mentee

# UI/UX tests
make test-ui-ux

# Full integration tests
make test-integration
```

### Browser-Specific Tests
```bash
# Run on Chrome only
make test-chrome

# Run on Firefox only
make test-firefox

# Run on Safari only
make test-safari
```

### Development and Debugging
```bash
# Debug mode (step through tests)
make test-debug

# Run with retries (for flaky tests)
make test-retry

# Run tests in parallel
make test-parallel
```

## Test Configuration

The tests are configured in `playwright.config.js` with the following features:

- **Multi-browser support**: Chrome, Firefox, Safari, Mobile Chrome, Mobile Safari
- **Automatic server startup**: Starts both backend and frontend servers
- **Screenshots on failure**: Captures visual evidence of test failures
- **Video recording**: Records test execution for failed tests
- **Trace collection**: Detailed execution traces for debugging

## Test Structure

Each test file follows a consistent structure:

```javascript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    // Setup code
  });

  test('should do something', async ({ page }) => {
    // Test implementation
  });
});
```

## Best Practices

### Test Data Management
- Uses timestamp-based unique identifiers for test users
- Cleans up test data automatically
- Isolates tests to prevent interference

### Page Object Pattern
Tests use data-testid attributes for reliable element selection:
```html
<button data-testid="submit-button">Submit</button>
```

### Assertions
Uses meaningful assertions with proper wait conditions:
```javascript
await expect(page.locator('[data-testid="success-message"]')).toContainText('Success');
```

## Viewing Test Results

### HTML Report
```bash
make report
```

### Real-time Monitoring
```bash
make test-ui
```

## Common Issues and Solutions

### Tests Failing Due to Server Not Running
Ensure both servers are running before executing tests:
```bash
# Terminal 1
cd backend && make run

# Terminal 2
cd frontend && npm start

# Terminal 3
make test
```

### Timeout Issues
If tests are timing out, increase the timeout in `playwright.config.js`:
```javascript
use: {
  timeout: 30000, // 30 seconds
}
```

### Browser Installation Issues
```bash
npx playwright install
```

## Test Data and State Management

- Each test creates its own unique test data using timestamps
- Tests are designed to be independent and can run in any order
- Database state is managed through the API to ensure consistency
- No external test database required - uses the same database as development

## CI/CD Integration

The tests are configured for CI/CD environments:
- Automatic retry on failure (2 retries in CI)
- Headless mode by default
- Parallel execution disabled in CI for stability
- Detailed reporting and artifacts

## Contributing

When adding new tests:

1. Follow the existing naming convention
2. Use data-testid attributes for element selection
3. Include proper assertions with wait conditions
4. Add test documentation in comments
5. Ensure tests are independent and can run in isolation

## Performance Considerations

- Tests run in parallel by default (except in CI)
- Each test creates minimal required data
- Tests clean up after themselves
- Video recording only on failure to save space
- Screenshots only on failure

## Security Testing

The test suite includes:
- Authentication flow validation
- JWT token handling
- Input validation testing
- Authorization checks
- CORS and security header validation

---

For more information about Playwright, visit: https://playwright.dev/

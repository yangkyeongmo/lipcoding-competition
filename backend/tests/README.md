# Backend Test Suite

Comprehensive test suite for the Mentor-Mentee Matching Backend API.

## Test Structure

### Test Files
- `test_auth.py` - Authentication endpoints (signup, login)
- `test_users.py` - User profile management and image upload
- `test_mentors.py` - Mentor listing, search, and filtering
- `test_matching.py` - Matching request CRUD operations
- `test_auth_utils.py` - Authentication utility functions
- `test_database.py` - Database models and relationships
- `test_integration.py` - End-to-end integration tests

### Test Fixtures
- `conftest.py` - Shared test fixtures and configuration
  - Database setup/teardown
  - Test clients (authenticated/unauthenticated)
  - Sample test data

## Running Tests

### All Tests
```bash
make test
```

### Specific Test File
```bash
pytest tests/test_auth.py -v
```

### Specific Test Class
```bash
pytest tests/test_auth.py::TestAuthentication -v
```

### Specific Test Method
```bash
pytest tests/test_auth.py::TestAuthentication::test_signup_success -v
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## Test Categories

### Unit Tests
- Authentication utilities
- Database models
- Individual endpoint functionality

### Integration Tests
- Complete user workflows
- Multi-endpoint interactions
- Data flow between components

### API Tests
- Request/response validation
- Authentication and authorization
- Error handling
- Status codes

## Test Coverage

The test suite covers:

✅ **Authentication**
- User signup with validation
- Login with JWT token generation
- Invalid credentials handling
- Token verification

✅ **User Management**
- Profile creation and updates
- Profile image upload
- Role-based restrictions
- Data validation

✅ **Mentor Features**
- Mentor listing and search
- Tech stack filtering
- Sorting functionality
- Access control (mentees only)

✅ **Matching System**
- Request creation and validation
- Status updates (accept/reject)
- Role-based operations
- Request deletion

✅ **Database Operations**
- Model relationships
- Data integrity
- Constraint validation
- CRUD operations

✅ **Security**
- JWT token validation
- Password hashing
- Role-based access control
- Input validation

## Test Data

Tests use isolated SQLite databases that are:
- Created fresh for each test
- Cleaned up automatically
- Independent of production data

## Mock Data

Sample test data includes:
- Test users (mentee/mentor)
- Sample profile images
- Matching requests
- Tech stacks

## Assertions

Tests verify:
- HTTP status codes
- Response data structure
- Database state changes
- Authentication tokens
- Error messages
- Business logic compliance

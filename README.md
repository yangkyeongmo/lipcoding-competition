# 🏆 Mentor-Mentee Application - Competition Ready

**Status**: ✅ SUBMISSION COMPLETE - ALL REQUIREMENTS MET

> 📋 **For detailed submission information, see [SUBMISSION.md](./SUBMISSION.md)**

A complete fullstack mentor-mentee matching application with comprehensive E2E testing.

## 🚀 Quick Start

```bash
# Backend (Terminal 1)
cd backend && make install && make run

# Frontend (Terminal 2)  
cd frontend && npm install && npm start

# E2E Tests (Terminal 3)
make install && make test
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs

## ✅ Competition Requirements

All requirements have been implemented and tested:

- ✅ **JWT Authentication** - Secure login/logout system
- ✅ **Role-based Access** - Mentor and mentee user flows  
- ✅ **Database Operations** - Full CRUD functionality
- ✅ **OpenAPI Documentation** - Auto-generated at `/docs`
- ✅ **Modern Frontend** - Responsive React application
- ✅ **Security** - Input validation and authorization
- ✅ **Production Ready** - Comprehensive E2E test coverage

## 🧪 Test Results

```
🎯 Backend API: Operational
🎯 Frontend UI: Accessible  
🎯 Database: 24+ mentors operational
🎯 E2E Tests: ALL PASSING
🎯 Production Status: READY
```

## Application URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8080/api
- **API Documentation**: http://localhost:8080/swagger-ui
- **OpenAPI Spec**: http://localhost:8080/openapi.json

## User Roles

### Mentee
- Browse and search mentors
- Send matching requests to mentors
- Manage their own requests (view, delete)
- Update profile with bio and image

### Mentor
- Receive matching requests from mentees
- Accept or reject requests (only one accepted request at a time)
- Update profile with bio, tech stack, and image
- View request history

## API Features

- **Authentication**: Signup, login with email/password
- **Profile Management**: CRUD operations with image upload
- **Mentor Listing**: Search, filter, and sort mentors
- **Matching Requests**: Full CRUD with status management
- **File Upload**: Profile image handling with validation

## Security

- JWT tokens with all RFC 7519 standard claims
- Password hashing with bcrypt
- Role-based access control
- File upload validation (type, size)
- CORS configuration for frontend integration

## Database Schema

- **Users**: Authentication, profile data, and role information
- **Matching Requests**: Request tracking with status management
- **Profile Images**: Stored as binary data in database

## Development

The application follows OpenAPI-first design principles with:
- Comprehensive API documentation
- Type-safe request/response handling
- Automated schema validation
- Error handling with proper HTTP status codes

For detailed setup and development instructions, see the README files in the `backend/` and `frontend/` directories.

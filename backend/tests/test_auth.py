import pytest
from fastapi import status

class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_signup_success(self, client, test_user_mentee):
        """Test successful user signup"""
        response = client.post("/api/signup", json=test_user_mentee)
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in response.json()
    
    def test_signup_duplicate_email(self, client, test_user_mentee):
        """Test signup with duplicate email"""
        # First signup
        client.post("/api/signup", json=test_user_mentee)
        
        # Second signup with same email
        response = client.post("/api/signup", json=test_user_mentee)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in response.json()["detail"]
    
    def test_signup_invalid_role(self, client):
        """Test signup with invalid role"""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User",
            "role": "invalid_role"
        }
        response = client.post("/api/signup", json=user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Role must be either 'mentor' or 'mentee'" in response.json()["detail"]
    
    def test_signup_missing_fields(self, client):
        """Test signup with missing required fields"""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
            # Missing name and role
        }
        response = client.post("/api/signup", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_login_success(self, client, test_user_mentee):
        """Test successful login"""
        # Create user first
        client.post("/api/signup", json=test_user_mentee)
        
        # Login
        login_data = {
            "email": test_user_mentee["email"],
            "password": test_user_mentee["password"]
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.json()
        
        # Verify token is a string
        token = response.json()["token"]
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_invalid_password(self, client, test_user_mentee):
        """Test login with wrong password"""
        # Create user first
        client.post("/api/signup", json=test_user_mentee)
        
        # Login with wrong password
        login_data = {
            "email": test_user_mentee["email"],
            "password": "wrongpassword"
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        login_data = {
            "email": "test@example.com"
            # Missing password
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

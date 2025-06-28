import pytest
from datetime import datetime, timedelta
from app.core.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    verify_token,
    authenticate_user
)
from app.database import User
from sqlalchemy.orm import Session

class TestAuthUtils:
    """Test authentication utility functions"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        
        # Should not verify with wrong password
        assert verify_password("wrongpassword", hashed) is False
    
    def test_create_access_token(self):
        """Test JWT token creation"""
        data = {
            "sub": "123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "mentee"
        }
        
        token = create_access_token(data)
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Token should contain encoded data
        assert "." in token  # JWT has dots separating parts
    
    def test_create_access_token_with_expiration(self):
        """Test JWT token creation with custom expiration"""
        data = {"sub": "123"}
        expires_delta = timedelta(minutes=30)
        
        token = create_access_token(data, expires_delta)
        assert isinstance(token, str)
        
        # Verify token contains correct expiration
        payload = verify_token(token)
        assert payload is not None
        
        # Check if expiration is approximately correct
        exp_timestamp = payload.get("exp")
        actual_exp = datetime.utcfromtimestamp(exp_timestamp)
        
        # Calculate expected expiration time 
        expected_exp = datetime.utcnow() + expires_delta
        
        # Allow reasonable tolerance (within 30 seconds) for processing time
        time_diff = abs((actual_exp - expected_exp).total_seconds())
        assert time_diff < 30, f"Time difference too large: {time_diff} seconds"
    
    def test_verify_token_valid(self):
        """Test token verification with valid token"""
        data = {
            "sub": "123",
            "email": "test@example.com",
            "name": "Test User",
            "role": "mentee"
        }
        
        token = create_access_token(data)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload["sub"] == "123"
        assert payload["email"] == "test@example.com"
        assert payload["name"] == "Test User"
        assert payload["role"] == "mentee"
        
        # Check JWT standard claims
        assert "iss" in payload  # Issuer
        assert "aud" in payload  # Audience
        assert "exp" in payload  # Expiration
        assert "nbf" in payload  # Not before
        assert "iat" in payload  # Issued at
        assert "jti" in payload  # JWT ID
        
        assert payload["iss"] == "mentor-mentee-app"
        assert payload["aud"] == "mentor-mentee-users"
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token"""
        invalid_token = "invalid.token.here"
        payload = verify_token(invalid_token)
        assert payload is None
    
    def test_verify_token_expired(self):
        """Test token verification with expired token"""
        data = {"sub": "123"}
        # Create token that expires immediately
        expires_delta = timedelta(seconds=-1)  # Already expired
        
        token = create_access_token(data, expires_delta)
        payload = verify_token(token)
        
        # Should be None due to expiration
        assert payload is None
    
    def test_authenticate_user_success(self, client):
        """Test user authentication with correct credentials"""
        # Use the override_get_db function to get test database session
        from tests.conftest import override_get_db
        from app.database import User
        from app.core.auth import get_password_hash
        
        # Get database session using the same method as the test fixtures
        db = next(override_get_db())
        try:
            hashed_password = get_password_hash("testpassword123")
            test_user = User(
                email="test@example.com",
                hashed_password=hashed_password,
                name="Test User",
                role="mentee"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
            # Test authentication
            authenticated_user = authenticate_user(db, "test@example.com", "testpassword123")
            assert authenticated_user is not None
            assert authenticated_user.email == "test@example.com"
            assert authenticated_user.name == "Test User"
        finally:
            db.close()
    
    def test_authenticate_user_wrong_email(self, client):
        """Test authentication with non-existent email"""
        from tests.conftest import override_get_db
        
        db = next(override_get_db())
        try:
            authenticated_user = authenticate_user(db, "nonexistent@example.com", "password")
            assert authenticated_user is None
        finally:
            db.close()
    
    def test_authenticate_user_wrong_password(self, client):
        """Test authentication with wrong password"""
        from tests.conftest import override_get_db
        from app.database import User
        from app.core.auth import get_password_hash
        
        # Create test user
        db = next(override_get_db())
        try:
            hashed_password = get_password_hash("correctpassword")
            test_user = User(
                email="test2@example.com",
                hashed_password=hashed_password,
                name="Test User 2",
                role="mentee"
            )
            db.add(test_user)
            db.commit()
            
            # Test with wrong password
            authenticated_user = authenticate_user(db, "test2@example.com", "wrongpassword")
            assert authenticated_user is None
        finally:
            db.close()

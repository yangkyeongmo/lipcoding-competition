import pytest
from datetime import datetime
from app.database import User, MatchingRequest

class TestDatabaseModels:
    """Test database models and their relationships"""
    
    def test_user_model_creation(self, client):
        """Test User model creation and attributes"""
        from app.database import TestingSessionLocal
        
        db = TestingSessionLocal()
        
        # Create a user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_here",
            name="Test User",
            role="mentee",
            bio="This is a test bio",
            tech_stack='["Python", "JavaScript"]'
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Test attributes
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.role == "mentee"
        assert user.bio == "This is a test bio"
        assert user.tech_stack == '["Python", "JavaScript"]'
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        
        db.close()
    
    def test_matching_request_model_creation(self, client):
        """Test MatchingRequest model creation and attributes"""
        from app.database import TestingSessionLocal
        
        db = TestingSessionLocal()
        
        # Create users first
        mentee = User(
            email="mentee@example.com",
            hashed_password="hashed_password",
            name="Test Mentee",
            role="mentee"
        )
        mentor = User(
            email="mentor@example.com",
            hashed_password="hashed_password",
            name="Test Mentor",
            role="mentor"
        )
        
        db.add(mentee)
        db.add(mentor)
        db.commit()
        db.refresh(mentee)
        db.refresh(mentor)
        
        # Create matching request
        matching_request = MatchingRequest(
            mentee_id=mentee.id,
            mentor_id=mentor.id,
            message="I would like to learn from you!",
            status="pending"
        )
        
        db.add(matching_request)
        db.commit()
        db.refresh(matching_request)
        
        # Test attributes
        assert matching_request.id is not None
        assert matching_request.mentee_id == mentee.id
        assert matching_request.mentor_id == mentor.id
        assert matching_request.message == "I would like to learn from you!"
        assert matching_request.status == "pending"
        assert isinstance(matching_request.created_at, datetime)
        assert isinstance(matching_request.updated_at, datetime)
        
        db.close()
    
    def test_user_email_uniqueness(self, client):
        """Test that user emails must be unique"""
        from app.database import TestingSessionLocal
        from sqlalchemy.exc import IntegrityError
        
        db = TestingSessionLocal()
        
        # Create first user
        user1 = User(
            email="duplicate@example.com",
            hashed_password="password1",
            name="User 1",
            role="mentee"
        )
        db.add(user1)
        db.commit()
        
        # Try to create second user with same email
        user2 = User(
            email="duplicate@example.com",
            hashed_password="password2",
            name="User 2",
            role="mentor"
        )
        db.add(user2)
        
        # Should raise integrity error
        with pytest.raises(IntegrityError):
            db.commit()
        
        db.rollback()
        db.close()
    
    def test_matching_request_status_values(self, client):
        """Test matching request with different status values"""
        from app.database import TestingSessionLocal
        
        db = TestingSessionLocal()
        
        # Create users
        mentee = User(
            email="mentee2@example.com",
            hashed_password="password",
            name="Mentee 2",
            role="mentee"
        )
        mentor = User(
            email="mentor2@example.com",
            hashed_password="password",
            name="Mentor 2",
            role="mentor"
        )
        
        db.add(mentee)
        db.add(mentor)
        db.commit()
        db.refresh(mentee)
        db.refresh(mentor)
        
        # Test different status values
        statuses = ["pending", "accepted", "rejected"]
        
        for status in statuses:
            matching_request = MatchingRequest(
                mentee_id=mentee.id,
                mentor_id=mentor.id,
                message=f"Request with {status} status",
                status=status
            )
            db.add(matching_request)
            db.commit()
            db.refresh(matching_request)
            
            assert matching_request.status == status
        
        db.close()
    
    def test_user_profile_image_storage(self, client):
        """Test storing profile image as binary data"""
        from app.database import TestingSessionLocal
        
        db = TestingSessionLocal()
        
        # Sample image data (small PNG)
        image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
        
        user = User(
            email="imageuser@example.com",
            hashed_password="password",
            name="Image User",
            role="mentee",
            profile_image=image_data,
            profile_image_filename="test.png"
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Test image storage
        assert user.profile_image == image_data
        assert user.profile_image_filename == "test.png"
        
        db.close()

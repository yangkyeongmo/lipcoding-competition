import pytest
from fastapi import status
import json
import io

class TestUserProfile:
    """Test user profile endpoints"""
    
    def test_get_current_user_success(self, authenticated_mentee_client):
        """Test getting current user profile"""
        response = authenticated_mentee_client.get("/api/me")
        assert response.status_code == status.HTTP_200_OK
        
        user_data = response.json()
        assert "id" in user_data
        assert "email" in user_data
        assert "name" in user_data
        assert "role" in user_data
        assert user_data["role"] == "mentee"
        assert "profile_image_url" in user_data
    
    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/api/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_profile_success(self, authenticated_mentee_client):
        """Test updating user profile"""
        update_data = {
            "name": "Updated Name",
            "bio": "This is my updated bio"
        }
        response = authenticated_mentee_client.put("/api/me", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        user_data = response.json()
        assert user_data["name"] == "Updated Name"
        assert user_data["bio"] == "This is my updated bio"
    
    def test_update_mentor_tech_stack(self, authenticated_mentor_client):
        """Test updating mentor tech stack"""
        update_data = {
            "name": "Updated Mentor",
            "bio": "Experienced mentor",
            "tech_stack": ["Python", "React", "JavaScript"]
        }
        response = authenticated_mentor_client.put("/api/me", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        user_data = response.json()
        assert user_data["tech_stack"] == ["Python", "React", "JavaScript"]
    
    def test_mentee_cannot_set_tech_stack(self, authenticated_mentee_client):
        """Test that mentees cannot set tech stack"""
        update_data = {
            "tech_stack": ["Python", "React"]
        }
        response = authenticated_mentee_client.put("/api/me", json=update_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Only mentors can have tech stack" in response.json()["detail"]
    
    def test_upload_profile_image_success(self, authenticated_mentee_client, sample_image):
        """Test successful profile image upload"""
        files = {
            "file": ("test.png", io.BytesIO(sample_image), "image/png")
        }
        response = authenticated_mentee_client.post("/api/me/profile-image", files=files)
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
    
    def test_upload_invalid_file_type(self, authenticated_mentee_client):
        """Test uploading invalid file type"""
        files = {
            "file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")
        }
        response = authenticated_mentee_client.post("/api/me/profile-image", files=files)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Only .jpg and .png files are allowed" in response.json()["detail"]
    
    def test_upload_large_file(self, authenticated_mentee_client):
        """Test uploading file that's too large"""
        # Create a file larger than 1MB
        large_image = b"x" * (1024 * 1024 + 1)  # 1MB + 1 byte
        files = {
            "file": ("large.png", io.BytesIO(large_image), "image/png")
        }
        response = authenticated_mentee_client.post("/api/me/profile-image", files=files)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "File size must be less than 1MB" in response.json()["detail"]
    
    def test_upload_image_unauthorized(self, client, sample_image):
        """Test uploading image without authentication"""
        files = {
            "file": ("test.png", io.BytesIO(sample_image), "image/png")
        }
        response = client.post("/api/me/profile-image", files=files)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

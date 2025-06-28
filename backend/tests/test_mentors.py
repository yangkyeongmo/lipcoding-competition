import pytest
from fastapi import status

class TestMentors:
    """Test mentor-related endpoints"""
    
    def test_get_mentors_as_mentee(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test getting mentor list as mentee"""
        # First, update mentor profile with tech stack
        mentor_update = {
            "name": "Test Mentor",
            "bio": "Experienced mentor in software development",
            "tech_stack": ["Python", "React", "JavaScript"]
        }
        authenticated_mentor_client.put("/api/me", json=mentor_update)
        
        # Now get mentors as mentee
        response = authenticated_mentee_client.get("/api/mentors")
        assert response.status_code == status.HTTP_200_OK
        
        mentors = response.json()
        assert isinstance(mentors, list)
        assert len(mentors) >= 1
        
        # Check mentor data structure
        mentor = mentors[0]
        assert "id" in mentor
        assert "name" in mentor
        assert "bio" in mentor
        assert "tech_stack" in mentor
        assert "profile_image_url" in mentor
    
    def test_get_mentors_unauthorized(self, client):
        """Test getting mentors without authentication"""
        response = client.get("/api/mentors")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_mentors_as_mentor_forbidden(self, authenticated_mentor_client):
        """Test that mentors cannot view mentor list"""
        response = authenticated_mentor_client.get("/api/mentors")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Only mentees can view mentor list" in response.json()["detail"]
    
    def test_search_mentors_by_name(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test searching mentors by name"""
        # Update mentor name
        authenticated_mentor_client.put("/api/me", json={"name": "John Doe"})
        
        # Search for mentor
        response = authenticated_mentee_client.get("/api/mentors?search=John")
        assert response.status_code == status.HTTP_200_OK
        
        mentors = response.json()
        assert len(mentors) >= 1
        assert "John" in mentors[0]["name"]
    
    def test_filter_mentors_by_tech_stack(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test filtering mentors by tech stack"""
        # Update mentor with specific tech stack
        mentor_update = {
            "tech_stack": ["Python", "Django", "PostgreSQL"]
        }
        authenticated_mentor_client.put("/api/me", json=mentor_update)
        
        # Filter by tech stack
        response = authenticated_mentee_client.get("/api/mentors?tech_stack=Python")
        assert response.status_code == status.HTTP_200_OK
        
        mentors = response.json()
        assert len(mentors) >= 1
        # Check if Python is in tech stack
        found_python = any("Python" in mentor.get("tech_stack", []) for mentor in mentors)
        assert found_python
    
    def test_sort_mentors_by_name(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test sorting mentors by name"""
        response = authenticated_mentee_client.get("/api/mentors?sort_by=name")
        assert response.status_code == status.HTTP_200_OK
        
        mentors = response.json()
        # Check if sorted (assuming at least one mentor)
        if len(mentors) > 1:
            names = [mentor["name"] for mentor in mentors]
            assert names == sorted(names)
    
    def test_sort_mentors_by_tech_stack(self, authenticated_mentee_client):
        """Test sorting mentors by tech stack"""
        response = authenticated_mentee_client.get("/api/mentors?sort_by=tech_stack")
        assert response.status_code == status.HTTP_200_OK
        # Should not fail even if sorting by tech_stack

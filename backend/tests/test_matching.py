import pytest
from fastapi import status

class TestMatchingRequests:
    """Test matching request endpoints"""
    
    def test_create_matching_request_success(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test creating a matching request"""
        # Get mentor ID from mentor profile
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        # Create matching request
        request_data = {
            "mentor_id": mentor_id,
            "message": "I would like to learn from you!"
        }
        response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        assert response.status_code == status.HTTP_200_OK
        
        request_response = response.json()
        assert "id" in request_response
        assert request_response["mentor_id"] == mentor_id
        assert request_response["message"] == "I would like to learn from you!"
        assert request_response["status"] == "pending"
    
    def test_create_matching_request_unauthorized(self, client):
        """Test creating matching request without authentication"""
        request_data = {
            "mentor_id": 1,
            "message": "Test message"
        }
        response = client.post("/api/matching-requests", json=request_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_mentor_cannot_create_request(self, authenticated_mentor_client):
        """Test that mentors cannot create matching requests"""
        request_data = {
            "mentor_id": 1,
            "message": "Test message"
        }
        response = authenticated_mentor_client.post("/api/matching-requests", json=request_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Only mentees can create matching requests" in response.json()["detail"]
    
    def test_create_request_nonexistent_mentor(self, authenticated_mentee_client):
        """Test creating request for non-existent mentor"""
        request_data = {
            "mentor_id": 99999,
            "message": "Test message"
        }
        response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Mentor not found" in response.json()["detail"]
    
    def test_duplicate_request_to_same_mentor(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test creating duplicate request to same mentor"""
        # Get mentor ID
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        # Create first request
        request_data = {
            "mentor_id": mentor_id,
            "message": "First request"
        }
        response1 = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        assert response1.status_code == status.HTTP_200_OK
        
        # Try to create second request to same mentor
        request_data["message"] = "Second request"
        response2 = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert "already sent a request to this mentor" in response2.json()["detail"]
    
    def test_get_matching_requests_as_mentee(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test getting matching requests as mentee (sent requests)"""
        # Create a request first
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        
        # Get requests
        response = authenticated_mentee_client.get("/api/matching-requests")
        assert response.status_code == status.HTTP_200_OK
        
        requests = response.json()
        assert isinstance(requests, list)
        assert len(requests) >= 1
        assert requests[0]["mentor_id"] == mentor_id
    
    def test_get_matching_requests_as_mentor(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test getting matching requests as mentor (received requests)"""
        # Create a request first
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        
        # Get requests as mentor
        response = authenticated_mentor_client.get("/api/matching-requests")
        assert response.status_code == status.HTTP_200_OK
        
        requests = response.json()
        assert isinstance(requests, list)
        assert len(requests) >= 1
        assert requests[0]["mentor_id"] == mentor_id
    
    def test_update_matching_request_accept(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test mentor accepting a matching request"""
        # Create request
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        create_response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        request_id = create_response.json()["id"]
        
        # Accept request
        update_data = {"status": "accepted"}
        response = authenticated_mentor_client.put(f"/api/matching-requests/{request_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        updated_request = response.json()
        assert updated_request["status"] == "accepted"
    
    def test_update_matching_request_reject(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test mentor rejecting a matching request"""
        # Create request
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        create_response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        request_id = create_response.json()["id"]
        
        # Reject request
        update_data = {"status": "rejected"}
        response = authenticated_mentor_client.put(f"/api/matching-requests/{request_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        updated_request = response.json()
        assert updated_request["status"] == "rejected"
    
    def test_mentee_cannot_update_request(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test that mentees cannot update matching requests"""
        # Create request
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        create_response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        request_id = create_response.json()["id"]
        
        # Try to update as mentee
        update_data = {"status": "accepted"}
        response = authenticated_mentee_client.put(f"/api/matching-requests/{request_id}", json=update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Only mentors can update matching requests" in response.json()["detail"]
    
    def test_delete_matching_request(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test deleting a matching request"""
        # Create request
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        create_response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        request_id = create_response.json()["id"]
        
        # Delete request
        response = authenticated_mentee_client.delete(f"/api/matching-requests/{request_id}")
        assert response.status_code == status.HTTP_200_OK
        assert "message" in response.json()
        
        # Verify request is deleted
        get_response = authenticated_mentee_client.get("/api/matching-requests")
        requests = get_response.json()
        request_ids = [req["id"] for req in requests]
        assert request_id not in request_ids
    
    def test_mentor_cannot_delete_request(self, authenticated_mentee_client, authenticated_mentor_client):
        """Test that mentors cannot delete matching requests"""
        # Create request
        mentor_response = authenticated_mentor_client.get("/api/me")
        mentor_id = mentor_response.json()["id"]
        
        request_data = {
            "mentor_id": mentor_id,
            "message": "Test request"
        }
        create_response = authenticated_mentee_client.post("/api/matching-requests", json=request_data)
        request_id = create_response.json()["id"]
        
        # Try to delete as mentor
        response = authenticated_mentor_client.delete(f"/api/matching-requests/{request_id}")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Only mentees can delete their matching requests" in response.json()["detail"]

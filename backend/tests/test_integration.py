import pytest
from fastapi import status

class TestIntegration:
    """Test complete application workflows"""
    
    def test_complete_mentee_workflow(self, client):
        """Test complete mentee workflow: signup -> login -> view mentors -> request matching"""
        
        # 1. Mentee signup
        mentee_data = {
            "email": "integration_mentee@example.com",
            "password": "testpassword123",
            "name": "Integration Mentee",
            "role": "mentee"
        }
        response = client.post("/api/signup", json=mentee_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # 2. Create a mentor for the test
        mentor_data = {
            "email": "integration_mentor@example.com",
            "password": "testpassword123",
            "name": "Integration Mentor",
            "role": "mentor"
        }
        client.post("/api/signup", json=mentor_data)
        
        # Login as mentor and update profile
        mentor_login = client.post("/api/login", json={
            "email": mentor_data["email"],
            "password": mentor_data["password"]
        })
        mentor_token = mentor_login.json()["token"]
        
        mentor_profile_update = {
            "name": "Experienced Mentor",
            "bio": "10 years of software development experience",
            "tech_stack": ["Python", "React", "AWS"]
        }
        client.put("/api/me", json=mentor_profile_update, headers={
            "Authorization": f"Bearer {mentor_token}"
        })
        
        # 3. Mentee login
        login_response = client.post("/api/login", json={
            "email": mentee_data["email"],
            "password": mentee_data["password"]
        })
        assert login_response.status_code == status.HTTP_200_OK
        mentee_token = login_response.json()["token"]
        
        # 4. Get mentee profile
        profile_response = client.get("/api/me", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert profile_response.status_code == status.HTTP_200_OK
        assert profile_response.json()["role"] == "mentee"
        
        # 5. Update mentee profile
        profile_update = {
            "name": "Updated Mentee Name",
            "bio": "I'm eager to learn programming"
        }
        update_response = client.put("/api/me", json=profile_update, headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["name"] == "Updated Mentee Name"
        
        # 6. View mentors
        mentors_response = client.get("/api/mentors", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert mentors_response.status_code == status.HTTP_200_OK
        mentors = mentors_response.json()
        assert len(mentors) >= 1
        
        # 7. Create matching request
        mentor_id = mentors[0]["id"]
        request_data = {
            "mentor_id": mentor_id,
            "message": "I would love to learn from your expertise!"
        }
        request_response = client.post("/api/matching-requests", json=request_data, headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert request_response.status_code == status.HTTP_200_OK
        request_id = request_response.json()["id"]
        
        # 8. Check mentee's requests
        mentee_requests = client.get("/api/matching-requests", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert mentee_requests.status_code == status.HTTP_200_OK
        assert len(mentee_requests.json()) >= 1
        
        # 9. Check mentor's received requests
        mentor_requests = client.get("/api/matching-requests", headers={
            "Authorization": f"Bearer {mentor_token}"
        })
        assert mentor_requests.status_code == status.HTTP_200_OK
        assert len(mentor_requests.json()) >= 1
        
        # 10. Mentor accepts the request
        accept_response = client.put(f"/api/matching-requests/{request_id}", 
                                   json={"status": "accepted"}, 
                                   headers={"Authorization": f"Bearer {mentor_token}"})
        assert accept_response.status_code == status.HTTP_200_OK
        assert accept_response.json()["status"] == "accepted"
    
    def test_complete_mentor_workflow(self, client):
        """Test complete mentor workflow: signup -> login -> receive request -> accept/reject"""
        
        # 1. Mentor signup
        mentor_data = {
            "email": "workflow_mentor@example.com",
            "password": "testpassword123",
            "name": "Workflow Mentor",
            "role": "mentor"
        }
        response = client.post("/api/signup", json=mentor_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # 2. Mentor login
        login_response = client.post("/api/login", json={
            "email": mentor_data["email"],
            "password": mentor_data["password"]
        })
        assert login_response.status_code == status.HTTP_200_OK
        mentor_token = login_response.json()["token"]
        
        # 3. Update mentor profile with tech stack
        profile_update = {
            "name": "Senior Software Engineer",
            "bio": "Passionate about mentoring junior developers",
            "tech_stack": ["JavaScript", "Node.js", "MongoDB", "Docker"]
        }
        update_response = client.put("/api/me", json=profile_update, headers={
            "Authorization": f"Bearer {mentor_token}"
        })
        assert update_response.status_code == status.HTTP_200_OK
        assert update_response.json()["tech_stack"] == profile_update["tech_stack"]
        
        # 4. Create mentee and send request
        mentee_data = {
            "email": "workflow_mentee@example.com",
            "password": "testpassword123",
            "name": "Workflow Mentee",
            "role": "mentee"
        }
        client.post("/api/signup", json=mentee_data)
        
        mentee_login = client.post("/api/login", json={
            "email": mentee_data["email"],
            "password": mentee_data["password"]
        })
        mentee_token = mentee_login.json()["token"]
        
        # Get mentor ID
        mentor_profile = client.get("/api/me", headers={
            "Authorization": f"Bearer {mentor_token}"
        })
        mentor_id = mentor_profile.json()["id"]
        
        # Send matching request
        request_data = {
            "mentor_id": mentor_id,
            "message": "I need guidance in JavaScript development"
        }
        request_response = client.post("/api/matching-requests", json=request_data, headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        request_id = request_response.json()["id"]
        
        # 5. Mentor checks received requests
        requests_response = client.get("/api/matching-requests", headers={
            "Authorization": f"Bearer {mentor_token}"
        })
        assert requests_response.status_code == status.HTTP_200_OK
        requests = requests_response.json()
        assert len(requests) >= 1
        assert requests[0]["status"] == "pending"
        
        # 6. Mentor rejects the request
        reject_response = client.put(f"/api/matching-requests/{request_id}", 
                                   json={"status": "rejected"}, 
                                   headers={"Authorization": f"Bearer {mentor_token}"})
        assert reject_response.status_code == status.HTTP_200_OK
        assert reject_response.json()["status"] == "rejected"
    
    def test_mentor_search_and_filtering(self, client):
        """Test mentor search and filtering functionality"""
        
        # Create multiple mentors with different profiles
        mentors_data = [
            {
                "email": "python_mentor@example.com",
                "password": "password123",
                "name": "Python Expert",
                "role": "mentor",
                "profile": {
                    "bio": "Python development specialist",
                    "tech_stack": ["Python", "Django", "PostgreSQL"]
                }
            },
            {
                "email": "react_mentor@example.com",
                "password": "password123",
                "name": "React Specialist",
                "role": "mentor",
                "profile": {
                    "bio": "Frontend React developer",
                    "tech_stack": ["React", "JavaScript", "TypeScript"]
                }
            },
            {
                "email": "fullstack_mentor@example.com",
                "password": "password123",
                "name": "Full Stack Developer",
                "role": "mentor",
                "profile": {
                    "bio": "Full stack development mentor",
                    "tech_stack": ["Python", "React", "Node.js", "AWS"]
                }
            }
        ]
        
        # Create and set up mentors
        for mentor_data in mentors_data:
            client.post("/api/signup", json=mentor_data)
            
            login_response = client.post("/api/login", json={
                "email": mentor_data["email"],
                "password": mentor_data["password"]
            })
            token = login_response.json()["token"]
            
            client.put("/api/me", json=mentor_data["profile"], headers={
                "Authorization": f"Bearer {token}"
            })
        
        # Create mentee for testing
        mentee_data = {
            "email": "search_mentee@example.com",
            "password": "password123",
            "name": "Search Mentee",
            "role": "mentee"
        }
        client.post("/api/signup", json=mentee_data)
        
        mentee_login = client.post("/api/login", json={
            "email": mentee_data["email"],
            "password": mentee_data["password"]
        })
        mentee_token = mentee_login.json()["token"]
        
        # Test search by name
        search_response = client.get("/api/mentors?search=Python", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert search_response.status_code == status.HTTP_200_OK
        mentors = search_response.json()
        assert any("Python" in mentor["name"] for mentor in mentors)
        
        # Test filter by tech stack
        filter_response = client.get("/api/mentors?tech_stack=React", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert filter_response.status_code == status.HTTP_200_OK
        mentors = filter_response.json()
        # Should find mentors with React in their tech stack
        react_mentors = [m for m in mentors if m["tech_stack"] and "React" in m["tech_stack"]]
        assert len(react_mentors) >= 1
        
        # Test sorting by name
        sort_response = client.get("/api/mentors?sort_by=name", headers={
            "Authorization": f"Bearer {mentee_token}"
        })
        assert sort_response.status_code == status.HTTP_200_OK
        mentors = sort_response.json()
        names = [mentor["name"] for mentor in mentors]
        assert names == sorted(names)

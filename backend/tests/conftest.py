import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

from app.main import app
from app.database import get_db, Base
from app.core.auth import get_current_user

# Create temporary database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user_mentee():
    return {
        "email": "mentee@example.com",
        "password": "testpassword123",
        "name": "Test Mentee",
        "role": "mentee"
    }

@pytest.fixture
def test_user_mentor():
    return {
        "email": "mentor@example.com",
        "password": "testpassword123",
        "name": "Test Mentor",
        "role": "mentor"
    }

@pytest.fixture
def authenticated_mentee_client(test_user_mentee):
    # Create a fresh client instance for mentee
    Base.metadata.create_all(bind=engine)
    mentee_client = TestClient(app)
    
    # Create user
    mentee_client.post("/api/signup", json=test_user_mentee)
    
    # Login and get token
    response = mentee_client.post("/api/login", json={
        "email": test_user_mentee["email"],
        "password": test_user_mentee["password"]
    })
    token = response.json()["token"]
    
    # Set authorization header
    mentee_client.headers.update({"Authorization": f"Bearer {token}"})
    yield mentee_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def authenticated_mentor_client(test_user_mentor):
    # Create a fresh client instance for mentor
    Base.metadata.create_all(bind=engine)
    mentor_client = TestClient(app)
    
    # Create user
    mentor_client.post("/api/signup", json=test_user_mentor)
    
    # Login and get token
    response = mentor_client.post("/api/login", json={
        "email": test_user_mentor["email"],
        "password": test_user_mentor["password"]
    })
    token = response.json()["token"]
    
    # Set authorization header
    mentor_client.headers.update({"Authorization": f"Bearer {token}"})
    yield mentor_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_image():
    # Create a small test image (1x1 PNG)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    return png_data

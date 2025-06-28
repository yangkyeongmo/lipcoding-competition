from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Auth schemas
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str  # "mentor" or "mentee"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str

# User schemas  
class UserProfileData(BaseModel):
    """Profile data nested within user response"""
    name: Optional[str] = None
    bio: Optional[str] = None
    imageUrl: Optional[str] = None  # Changed from profile_image_url to match API spec
    skills: Optional[List[str]] = None  # Changed from tech_stack to skills to match API spec

class UserProfile(BaseModel):
    id: int
    email: str
    role: str
    profile: UserProfileData  # Make this required to match API spec
    
    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[str] = None  # Base64 encoded image string per API spec
    skills: Optional[List[str]] = None  # Changed from tech_stack to skills
    role: Optional[str] = None

class UpdateMentorProfileRequest(BaseModel):
    """Mentor profile update request per OpenAPI spec"""
    id: int
    name: str
    role: str
    bio: str
    image: str  # Base64 encoded image string
    skills: List[str]

class UpdateMenteeProfileRequest(BaseModel):
    """Mentee profile update request per OpenAPI spec"""
    id: int
    name: str
    role: str
    bio: str
    image: str  # Base64 encoded image string

# Mentor schemas
class MentorListItem(BaseModel):
    id: int
    email: str  # Add email field per API spec
    role: str
    profile: UserProfileData  # Make this required to match API spec

    class Config:
        from_attributes = True

# Matching schemas
class MatchingRequestCreate(BaseModel):
    mentorId: int  # Changed from mentor_id to mentorId per API spec
    menteeId: int  # Add menteeId field per API spec
    message: str  # Required per API spec

class MatchingRequestResponse(BaseModel):
    id: int
    mentorId: int  # Changed from mentor_id to mentorId per API spec  
    menteeId: int  # Changed from mentee_id to menteeId per API spec
    message: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class MatchingRequestOutgoing(BaseModel):
    """Outgoing match requests (no message field per API spec)"""
    id: int
    mentorId: int
    menteeId: int
    status: str

    class Config:
        from_attributes = True

class MatchingRequestUpdate(BaseModel):
    status: str  # "accepted" or "rejected"

# Error schema
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None

# Export all schemas
__all__ = [
    "SignupRequest", "LoginRequest", "LoginResponse",
    "UserProfile", "UserProfileData", "UserProfileUpdate", 
    "UpdateMentorProfileRequest", "UpdateMenteeProfileRequest",
    "MentorListItem", 
    "MatchingRequestCreate", "MatchingRequestResponse", "MatchingRequestOutgoing", "MatchingRequestUpdate",
    "ErrorResponse"
]

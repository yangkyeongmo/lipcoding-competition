from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

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
    bio: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    profile_image_url: Optional[str] = None

class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    role: str
    bio: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    profile_image_url: Optional[str] = None
    profile: Optional[UserProfileData] = None  # For backward compatibility with tests
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    tech_stack: Optional[List[str]] = None

# Mentor schemas
class MentorListItem(BaseModel):
    id: int
    name: str
    role: str
    bio: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    profile_image_url: Optional[str] = None
    profile: Optional[UserProfileData] = None  # For backward compatibility with tests

    class Config:
        from_attributes = True

# Matching schemas
class MatchingRequestCreate(BaseModel):
    mentor_id: int
    message: Optional[str] = None

class MatchingRequestResponse(BaseModel):
    id: int
    mentee_id: int
    mentor_id: int
    message: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MatchingRequestUpdate(BaseModel):
    status: str  # "accepted" or "rejected"

# Error schema
class ErrorResponse(BaseModel):
    detail: str

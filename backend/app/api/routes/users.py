from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
import json
import base64

from app.database import get_db, User
from app.schemas import UserProfile, UserProfileUpdate
from app.core.auth import get_current_user

router = APIRouter()

def get_profile_image_url(user: User) -> Optional[str]:
    """Get profile image URL for user"""
    if user.profile_image:
        return f"data:image/{user.profile_image_filename.split('.')[-1]};base64,{base64.b64encode(user.profile_image).decode()}"
    else:
        # Return default placeholder image
        if user.role == "mentor":
            return "https://placehold.co/500x500.jpg?text=MENTOR"
        else:
            return "https://placehold.co/500x500.jpg?text=MENTEE"

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    tech_stack = None
    if current_user.tech_stack:
        try:
            tech_stack = json.loads(current_user.tech_stack)
        except json.JSONDecodeError:
            tech_stack = []
    
    profile_image_url = get_profile_image_url(current_user)
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        bio=current_user.bio,
        tech_stack=tech_stack,
        profile_image_url=profile_image_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.put("/me", response_model=UserProfile)
async def update_current_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    # Update fields if provided
    if profile_update.name is not None:
        current_user.name = profile_update.name
    
    if profile_update.bio is not None:
        current_user.bio = profile_update.bio
    
    if profile_update.tech_stack is not None:
        # Only mentors can have tech stack
        if current_user.role == "mentor":
            current_user.tech_stack = json.dumps(profile_update.tech_stack)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only mentors can have tech stack"
            )
    
    db.commit()
    db.refresh(current_user)
    
    # Return updated profile
    tech_stack = None
    if current_user.tech_stack:
        try:
            tech_stack = json.loads(current_user.tech_stack)
        except json.JSONDecodeError:
            tech_stack = []
    
    profile_image_url = get_profile_image_url(current_user)
    
    return UserProfile(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        bio=current_user.bio,
        tech_stack=tech_stack,
        profile_image_url=profile_image_url,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )

@router.post("/me/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload profile image"""
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .jpg and .png files are allowed"
        )
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size (max 1MB)
    if len(file_content) > 1024 * 1024:  # 1MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 1MB"
        )
    
    # Store image in database
    current_user.profile_image = file_content
    current_user.profile_image_filename = file.filename
    
    db.commit()
    
    return {"message": "Profile image uploaded successfully"}

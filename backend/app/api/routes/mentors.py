from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import base64

from app.database import get_db, User
from app.schemas import MentorListItem
from app.core.auth import get_current_user

router = APIRouter()

def get_profile_image_url(user: User) -> Optional[str]:
    """Get profile image URL for user"""
    if user.profile_image:
        return f"data:image/{user.profile_image_filename.split('.')[-1]};base64,{base64.b64encode(user.profile_image).decode()}"
    else:
        return "https://placehold.co/500x500.jpg?text=MENTOR"

@router.get("/mentors", response_model=List[MentorListItem])
async def get_mentors(
    tech_stack: Optional[str] = Query(None, description="Filter by tech stack"),
    search: Optional[str] = Query(None, description="Search by name"),
    sort_by: Optional[str] = Query("name", description="Sort by field (name, tech_stack)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of mentors with optional filtering and sorting"""
    # Only mentees can view mentors list
    if current_user.role != "mentee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentees can view mentors list"
        )
    
    # Build query
    query = db.query(User).filter(User.role == "mentor")
    
    # Apply filters
    if tech_stack:
        query = query.filter(User.tech_stack.like(f'%"{tech_stack}"%'))
    
    if search:
        query = query.filter(User.name.like(f'%{search}%'))
    
    # Apply sorting
    if sort_by == "name":
        query = query.order_by(User.name)
    elif sort_by == "tech_stack":
        query = query.order_by(User.tech_stack)
    
    mentors = query.all()
    
    # Convert to response format
    mentor_list = []
    for mentor in mentors:
        tech_stack_list = None
        if mentor.tech_stack:
            try:
                tech_stack_list = json.loads(mentor.tech_stack)
            except json.JSONDecodeError:
                tech_stack_list = []
        
        profile_image_url = get_profile_image_url(mentor)
        
        mentor_list.append(MentorListItem(
            id=mentor.id,
            name=mentor.name,
            role=mentor.role,
            bio=mentor.bio,
            tech_stack=tech_stack_list,
            profile_image_url=profile_image_url
        ))
    
    return mentor_list

@router.get("/mentors/{mentor_id}", response_model=MentorListItem)
async def get_mentor_by_id(
    mentor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific mentor by ID"""
    # Only mentees can view mentor details
    if current_user.role != "mentee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentees can view mentor details"
        )
    
    mentor = db.query(User).filter(User.id == mentor_id, User.role == "mentor").first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mentor not found"
        )
    
    tech_stack_list = None
    if mentor.tech_stack:
        try:
            tech_stack_list = json.loads(mentor.tech_stack)
        except json.JSONDecodeError:
            tech_stack_list = []
    
    profile_image_url = get_profile_image_url(mentor)
    
    return MentorListItem(
        id=mentor.id,
        name=mentor.name,
        role=mentor.role,
        bio=mentor.bio,
        tech_stack=tech_stack_list,
        profile_image_url=profile_image_url
    )

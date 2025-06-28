from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.database import get_db, User
from app.schemas import MentorListItem
from app.core.auth import get_current_user

router = APIRouter()

def get_profile_image_url(user: User) -> str:
    """Get profile image URL for user"""
    return f"/images/{user.role}/{user.id}"

@router.get("/mentors", response_model=List[MentorListItem])
async def get_mentors(
    tech_stack: Optional[str] = Query(None, description="Filter by tech stack"),
    skill: Optional[str] = Query(None, description="Filter by skill (alias for tech_stack)"),
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
    filter_skill = tech_stack or skill  # Use tech_stack or skill parameter
    if filter_skill:
        # Filter mentors who have the specified tech_stack/skill
        # First, get all mentors with tech_stack
        mentors_with_tech = query.filter(User.tech_stack.isnot(None)).all()
        filtered_mentors = []
        for mentor in mentors_with_tech:
            try:
                tech_list = json.loads(mentor.tech_stack) if mentor.tech_stack else []
                if filter_skill in tech_list:
                    filtered_mentors.append(mentor)
            except json.JSONDecodeError:
                continue
        
        # If no mentors found with the skill, return empty list
        if not filtered_mentors:
            return []
        
        # Convert to query with specific IDs
        mentor_ids = [m.id for m in filtered_mentors]
        query = query.filter(User.id.in_(mentor_ids))
    
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
        
        # Create profile data according to API spec
        profile_data = {
            "name": mentor.name,
            "bio": mentor.bio,
            "imageUrl": profile_image_url,
            "skills": tech_stack_list
        }
        
        mentor_list.append(MentorListItem(
            id=mentor.id,
            email=mentor.email,
            role=mentor.role,
            profile=profile_data
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
    
    # Create profile data according to API spec
    profile_data = {
        "name": mentor.name,
        "bio": mentor.bio,
        "imageUrl": profile_image_url,
        "skills": tech_stack_list
    }
    
    return MentorListItem(
        id=mentor.id,
        email=mentor.email,
        role=mentor.role,
        profile=profile_data
    )

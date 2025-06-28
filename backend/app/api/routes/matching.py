from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, User, MatchingRequest
from app.schemas import MatchingRequestCreate, MatchingRequestResponse, MatchingRequestUpdate, MatchingRequestOutgoing
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/match-requests", response_model=MatchingRequestResponse)
async def create_matching_request(
    request_data: MatchingRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new matching request (mentee to mentor)"""
    # Only mentees can create matching requests
    if current_user.role != "mentee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only mentees can create matching requests"}
        )
    
    # Check if mentor exists
    mentor = db.query(User).filter(User.id == request_data.mentorId, User.role == "mentor").first()
    if not mentor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Mentor not found"}
        )
    
    # Validate that menteeId matches current user
    if request_data.menteeId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "menteeId must match current authenticated user"}
        )
    
    # Check if mentee already sent a request to this mentor
    existing_mentor_request = db.query(MatchingRequest).filter(
        MatchingRequest.mentee_id == current_user.id,
        MatchingRequest.mentor_id == request_data.mentorId
    ).first()
    
    if existing_mentor_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "You have already sent a request to this mentor"}
        )
    
    # Create matching request
    matching_request = MatchingRequest(
        mentee_id=current_user.id,
        mentor_id=request_data.mentorId,
        message=request_data.message,
        status="pending"
    )
    
    db.add(matching_request)
    db.commit()
    db.refresh(matching_request)
    
    return MatchingRequestResponse(
        id=matching_request.id,
        menteeId=matching_request.mentee_id,
        mentorId=matching_request.mentor_id,
        message=matching_request.message,
        status=matching_request.status
    )

@router.get("/match-requests", response_model=List[MatchingRequestResponse])
async def get_matching_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get matching requests for current user"""
    if current_user.role == "mentee":
        # Mentees see their sent requests
        requests = db.query(MatchingRequest).filter(
            MatchingRequest.mentee_id == current_user.id
        ).order_by(MatchingRequest.created_at.desc()).all()
    else:
        # Mentors see requests sent to them
        requests = db.query(MatchingRequest).filter(
            MatchingRequest.mentor_id == current_user.id
        ).order_by(MatchingRequest.created_at.desc()).all()
    
    return [
        MatchingRequestResponse(
            id=req.id,
            menteeId=req.mentee_id,
            mentorId=req.mentor_id,
            message=req.message,
            status=req.status
        )
        for req in requests
    ]

@router.put("/match-requests/{request_id}", response_model=MatchingRequestResponse)
async def update_matching_request(
    request_id: int,
    request_update: MatchingRequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update matching request status (mentor accepts/rejects)"""
    # Only mentors can update requests
    if current_user.role != "mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can update matching requests"
        )
    
    # Find the request
    matching_request = db.query(MatchingRequest).filter(
        MatchingRequest.id == request_id,
        MatchingRequest.mentor_id == current_user.id
    ).first()
    
    if not matching_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matching request not found"
        )
    
    # Validate status
    if request_update.status not in ["accepted", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'accepted' or 'rejected'"
        )
    
    # Check if mentor already has an accepted request
    if request_update.status == "accepted":
        existing_accepted = db.query(MatchingRequest).filter(
            MatchingRequest.mentor_id == current_user.id,
            MatchingRequest.status == "accepted"
        ).first()
        
        if existing_accepted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can only have one accepted matching request at a time"
            )
    
    # Update request
    matching_request.status = request_update.status
    db.commit()
    db.refresh(matching_request)
    
    return MatchingRequestResponse(
        id=matching_request.id,
        menteeId=matching_request.mentee_id,
        mentorId=matching_request.mentor_id,
        message=matching_request.message,
        status=matching_request.status
    )

@router.get("/match-requests/incoming", response_model=List[MatchingRequestResponse])
async def get_incoming_matching_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get incoming matching requests (for mentors)"""
    if current_user.role != "mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can view incoming requests"
        )
    
    requests = db.query(MatchingRequest).filter(
        MatchingRequest.mentor_id == current_user.id
    ).order_by(MatchingRequest.created_at.desc()).all()
    
    return [
        MatchingRequestResponse(
            id=req.id,
            menteeId=req.mentee_id,
            mentorId=req.mentor_id,
            message=req.message,
            status=req.status
        )
        for req in requests
    ]

@router.get("/match-requests/outgoing", response_model=List[MatchingRequestOutgoing])
async def get_outgoing_matching_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get outgoing matching requests (for mentees)"""
    if current_user.role != "mentee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "Only mentees can view outgoing requests"}
        )
    
    requests = db.query(MatchingRequest).filter(
        MatchingRequest.mentee_id == current_user.id
    ).order_by(MatchingRequest.created_at.desc()).all()
    
    return [
        MatchingRequestOutgoing(
            id=req.id,
            menteeId=req.mentee_id,
            mentorId=req.mentor_id,
            status=req.status
        )
        for req in requests
    ]

@router.delete("/match-requests/{request_id}")
async def delete_matching_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete matching request (mentee cancels their request)"""
    # Only mentees can delete their own requests
    if current_user.role != "mentee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentees can delete their matching requests"
        )
    
    # Find the request
    matching_request = db.query(MatchingRequest).filter(
        MatchingRequest.id == request_id,
        MatchingRequest.mentee_id == current_user.id
    ).first()
    
    if not matching_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matching request not found"
        )
    
    # Return the cancelled request format per API spec
    response = MatchingRequestResponse(
        id=matching_request.id,
        mentorId=matching_request.mentor_id,
        menteeId=matching_request.mentee_id,
        message=matching_request.message,
        status="cancelled"
    )
    
    # Delete the request
    db.delete(matching_request)
    db.commit()
    
    return response

@router.put("/match-requests/{request_id}/accept", response_model=MatchingRequestResponse)
async def accept_matching_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a matching request (mentor accepts)"""
    # Only mentors can accept requests
    if current_user.role != "mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can accept matching requests"
        )
    
    # Find the request
    matching_request = db.query(MatchingRequest).filter(
        MatchingRequest.id == request_id,
        MatchingRequest.mentor_id == current_user.id
    ).first()
    
    if not matching_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matching request not found"
        )
    
    # Check if mentor already has an accepted request
    existing_accepted = db.query(MatchingRequest).filter(
        MatchingRequest.mentor_id == current_user.id,
        MatchingRequest.status == "accepted"
    ).first()
    
    if existing_accepted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only have one accepted matching request at a time"
        )
    
    # Accept the request
    matching_request.status = "accepted"
    db.commit()
    db.refresh(matching_request)
    
    return MatchingRequestResponse(
        id=matching_request.id,
        menteeId=matching_request.mentee_id,
        mentorId=matching_request.mentor_id,
        message=matching_request.message,
        status=matching_request.status
    )

@router.put("/match-requests/{request_id}/reject", response_model=MatchingRequestResponse)
async def reject_matching_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a matching request (mentor rejects)"""
    # Only mentors can reject requests
    if current_user.role != "mentor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only mentors can reject matching requests"
        )
    
    # Find the request
    matching_request = db.query(MatchingRequest).filter(
        MatchingRequest.id == request_id,
        MatchingRequest.mentor_id == current_user.id
    ).first()
    
    if not matching_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Matching request not found"
        )
    
    # Reject the request
    matching_request.status = "rejected"
    db.commit()
    db.refresh(matching_request)
    
    return MatchingRequestResponse(
        id=matching_request.id,
        menteeId=matching_request.mentee_id,
        mentorId=matching_request.mentor_id,
        message=matching_request.message,
        status=matching_request.status
    )

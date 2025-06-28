from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import re

from app.database import get_db, User
from app.schemas import SignupRequest, LoginRequest, LoginResponse
from app.core.auth import authenticate_user, create_access_token, get_password_hash
from app.core.config import settings

router = APIRouter()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Validate email format
    if not validate_email(signup_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == signup_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate role
    if signup_data.role not in ["mentor", "mentee"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'mentor' or 'mentee'"
        )
    
    # Create new user
    hashed_password = get_password_hash(signup_data.password)
    db_user = User(
        email=signup_data.email,
        hashed_password=hashed_password,
        name=signup_data.name,
        role=signup_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "User created successfully"}

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create JWT token with required claims
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    
    return {"token": access_token}

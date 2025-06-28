from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, LargeBinary, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "mentor" or "mentee"
    bio = Column(Text, nullable=True)
    tech_stack = Column(String, nullable=True)  # JSON string for mentors
    profile_image = Column(LargeBinary, nullable=True)
    profile_image_filename = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MatchingRequest(Base):
    __tablename__ = "matching_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    mentee_id = Column(Integer, nullable=False)
    mentor_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String, default="pending")  # "pending", "accepted", "rejected"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

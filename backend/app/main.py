from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.api.routes import auth, users, mentors, matching
from app.database import init_db

# Initialize database on startup
init_db()

app = FastAPI(
    title="Mentor-Mentee Matching API",
    description="API for matching mentors and mentees in a mentoring platform",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/swagger-ui",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Mount static files for profile images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routes
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(users.router, prefix="/api", tags=["User Profile"])
app.include_router(mentors.router, prefix="/api", tags=["Mentors"])
app.include_router(matching.router, prefix="/api", tags=["Matching"])

@app.get("/", include_in_schema=False)
async def root():
    """Redirect root URL to Swagger UI"""
    return RedirectResponse(url="/swagger-ui")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

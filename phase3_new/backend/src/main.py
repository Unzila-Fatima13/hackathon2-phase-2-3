from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from database.database import get_session
from api import auth, tasks, chatbot
from core.config import settings

# Create the FastAPI app
app = FastAPI(
    title="Todo App API",
    description="A full-stack multi-user todo application with secure authentication",
    version="1.0.0"
)

# Add CORS middleware
# Parse the BACKEND_CORS_ORIGINS from settings
cors_origins = []
if settings.BACKEND_CORS_ORIGINS:
    cors_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Specify allowed methods
    allow_headers=["X-Requested-With", "Content-Type", "Accept", "Origin", "Authorization"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
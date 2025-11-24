from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine, Base

# Import all models to ensure they're registered with SQLAlchemy
from app.models import user, social, tree, forum, notifications, nursery

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🌱 Starting KijaniCare360 API...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")
    
    yield
    
    # Shutdown
    print("🌳 Shutting down KijaniCare360 API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="KijaniCare360 - Tree Conservation Platform for Kenya 🌳",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "http://localhost:3000",  # Alternative local port
        "https://kijanicare-360.vercel.app",  # Vercel frontend
        settings.FRONTEND_URL,    # Production frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for uploaded images, etc.)
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to KijaniCare360 API 🌳",
        "version": settings.VERSION,
        "description": "Tree Conservation Platform for Kenya",
        "features": [
            "🌱 Tree Planting Streaks & Collaborative Challenges",
            "🤖 AI-Powered Tree Expert Chatbot",
            "📊 Kenya Forest Coverage Analytics",
            "👥 Community Forum & Social Following",
            "🏆 Gamification & Achievement System",
            "📅 Smart Calendar & Event Management",
            "🔔 Intelligent Notifications System",
            "📱 Social Posts & Community Feed"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "api": "/api/v1",
            "health": "/api/v1/health"
        },
        "regions_supported": [
            "Central Kenya", "Western Kenya", "Eastern Kenya",
            "Rift Valley", "Coast", "Nyanza", "Northern Kenya"
        ],
        "tree_species": 8,
        "languages": ["English", "Swahili"]
    }

@app.get("/api/v1")
def api_info():
    return {
        "service": "KijaniCare360 API",
        "version": settings.VERSION,
        "status": "operational",
        "endpoints": {
            "auth": "/api/v1/auth",
            "dashboard": "/api/v1/dashboard",
            "social": "/api/v1/social",
            "forum": "/api/v1/forum",
            "analytics": "/api/v1/analytics", 
            "chatbot": "/api/v1/chatbot",
            "notifications": "/api/v1/notifications",
            "trees": "/api/v1/trees"
        }
    }
from fastapi import APIRouter
from app.api.v1.endpoints import (
    simple_forum, analytics, notifications, chatbot, trees, auth, social, dashboard, frontend_analytics, profile, calendar, community_features
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    simple_forum.router,
    prefix="/forum",
    tags=["Community Forum"]
)

api_router.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics & Statistics"]
)

api_router.include_router(
    notifications.router,
    prefix="/notifications",
    tags=["Notifications"]
)

api_router.include_router(
    chatbot.router,
    prefix="/chatbot",
    tags=["AI Tree Expert"]
)

api_router.include_router(
    trees.router,
    prefix="/trees",
    tags=["Tree Management"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    social.router,
    prefix="/social",
    tags=["Social Features & Streaks"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["User Dashboard"]
)

api_router.include_router(
    frontend_analytics.router,
    prefix="/frontend-analytics",
    tags=["Frontend Analytics"]
)

api_router.include_router(
    profile.router,
    prefix="/profile",
    tags=["User Profile"]
)

api_router.include_router(
    calendar.router,
    prefix="/calendar",
    tags=["Tree Calendar & Events"]
)

api_router.include_router(
    community_features.router,
    prefix="/community",
    tags=["Community Features"]
)

# Health check endpoint
@api_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KijaniCare360 API",
        "version": "1.0.0",
        "features": [
            "Community Forum",
            "Tree Planting Streaks",
            "AI Tree Expert Chatbot",
            "Analytics Dashboard",
            "Notifications System"
        ]
    }
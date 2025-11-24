from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

router = APIRouter()

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get forum categories - simplified version"""
    # Return static data for now to avoid model relationship issues
    categories = [
        {
            "id": 1,
            "name": "Tree Planting Tips",
            "description": "Share and learn tree planting techniques",
            "icon": "🌱",
            "total_posts": 45,
            "total_topics": 12
        },
        {
            "id": 2,
            "name": "Species Discussion",
            "description": "Discuss different tree species for Kenya",
            "icon": "🌳",
            "total_posts": 78,
            "total_topics": 23
        },
        {
            "id": 3,
            "name": "Regional Groups",
            "description": "Connect with tree planters in your region",
            "icon": "🗺️",
            "total_posts": 34,
            "total_topics": 8
        },
        {
            "id": 4,
            "name": "Success Stories",
            "description": "Share your tree growing achievements",
            "icon": "🏆",
            "total_posts": 56,
            "total_topics": 19
        }
    ]
    
    return categories

@router.get("/stats")
def get_forum_stats():
    """Get forum statistics"""
    return {
        "total_topics": 62,
        "total_posts": 213,
        "total_users": 156,
        "active_streaks": 89
    }

@router.get("/leaderboard")
def get_community_leaderboard():
    """Get community leaderboard"""
    # Static data for demo
    leaderboard = [
        {
            "user_id": 1,
            "username": "TreeMaster_KE",
            "total_trees": 45,
            "streak_count": 3,
            "avatar_url": None
        },
        {
            "user_id": 2,
            "username": "GreenThumb_Nairobi",
            "total_trees": 38,
            "streak_count": 2,
            "avatar_url": None
        },
        {
            "user_id": 3,
            "username": "ForestGuardian",
            "total_trees": 32,
            "streak_count": 4,
            "avatar_url": None
        }
    ]
    
    return leaderboard
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.session import get_db
from app.models.user import User
from app.models.forum import TreePlantingStreak, UserAchievement, Achievement
from app.models.social import StreakActivity
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive user profile data"""
    
    # Get user streak
    streak = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id
    ).first()
    
    if not streak:
        streak = TreePlantingStreak(user_id=current_user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    
    # Get recent activities
    recent_activities = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id
    ).order_by(desc(StreakActivity.created_at)).limit(10).all()
    
    # Get achievements
    user_achievements = db.query(UserAchievement, Achievement).join(Achievement).filter(
        UserAchievement.user_id == current_user.id
    ).all()
    
    achievements = []
    for user_ach, achievement in user_achievements:
        achievements.append({
            "id": achievement.id,
            "title": achievement.name,
            "description": achievement.description,
            "icon": achievement.icon,
            "earned": True,
            "date": user_ach.earned_at.isoformat()
        })
    
    # Calculate goals progress
    goals = [
        {
            "id": 1,
            "title": "Plant 50 trees this year",
            "progress": min(current_user.total_trees_planted, 50),
            "target": 50,
            "type": "planting"
        },
        {
            "id": 2,
            "title": "Maintain 95% survival rate",
            "progress": 92,  # Mock data
            "target": 95,
            "type": "care"
        },
        {
            "id": 3,
            "title": "Join 5 community events",
            "progress": 2,  # Mock data
            "target": 5,
            "type": "community"
        }
    ]
    
    return {
        "username": current_user.username,
        "email": current_user.email,
        "location": current_user.location,
        "phone": current_user.phone_number,
        "bio": "Passionate about tree conservation and environmental sustainability.",
        "joinDate": current_user.created_at.isoformat(),
        "stats": {
            "treesPlanted": current_user.total_trees_planted,
            "treesAlive": int(current_user.total_trees_planted * 0.9),  # 90% survival
            "carbonOffset": int(current_user.total_trees_planted * 6.5),  # ~6.5kg per tree
            "communityRank": 15,  # Mock data
            "streakDays": streak.current_streak
        },
        "achievements": achievements,
        "recentActivities": [
            {
                "id": activity.id,
                "type": activity.activity_type,
                "description": f"{activity.activity_type.title()} {activity.trees_count} trees",
                "date": activity.created_at.strftime("%Y-%m-%d"),
                "location": activity.location or "Unknown"
            }
            for activity in recent_activities
        ],
        "goals": goals
    }

@router.put("/me")
def update_user_profile(
    profile_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    
    # Update allowed fields
    if "username" in profile_data:
        current_user.username = profile_data["username"]
    if "location" in profile_data:
        current_user.location = profile_data["location"]
    if "phone" in profile_data:
        current_user.phone_number = profile_data["phone"]
    
    db.commit()
    
    return {"message": "Profile updated successfully"}
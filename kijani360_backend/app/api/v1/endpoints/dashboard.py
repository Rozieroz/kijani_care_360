from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta

from app.database.session import get_db
from app.models.user import User
from app.models.social import (
    StreakActivity, CollaborativeStreak, CollaborativeStreakMember,
    CommunityEvent, EventAttendee, UserPost
)
from app.models.forum import TreePlantingStreak, UserAchievement, Achievement
from app.schemas.social import (
    UserDashboard, TreePlantingStreakResponse, StreakActivityResponse,
    UserAchievementResponse, AchievementResponse, CollaborativeStreakResponse,
    CommunityEventResponse
)
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=UserDashboard)
def get_user_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive user dashboard with all social features"""
    
    # User Statistics
    user_stats = {
        "trees_planted": current_user.total_trees_planted,
        "points": current_user.points,
        "level": current_user.level,
        "member_since": current_user.created_at.strftime("%B %Y"),
        "last_activity": None
    }
    
    # Get last activity
    last_activity = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id
    ).order_by(desc(StreakActivity.created_at)).first()
    
    if last_activity:
        user_stats["last_activity"] = last_activity.created_at
    
    # Streak Information
    streak = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id
    ).first()
    
    if not streak:
        streak = TreePlantingStreak(user_id=current_user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    
    streak_info = TreePlantingStreakResponse.from_orm(streak)
    
    # Recent Activities (last 10)
    recent_activities = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id
    ).order_by(desc(StreakActivity.created_at)).limit(10).all()
    
    activities_response = [StreakActivityResponse.from_orm(activity) for activity in recent_activities]
    
    # User Achievements
    user_achievements = db.query(UserAchievement, Achievement).join(Achievement).filter(
        UserAchievement.user_id == current_user.id
    ).order_by(desc(UserAchievement.earned_at)).all()
    
    achievements_response = []
    for user_ach, achievement in user_achievements:
        achievement_data = AchievementResponse.from_orm(achievement)
        achievements_response.append(UserAchievementResponse(
            id=user_ach.id,
            achievement=achievement_data,
            earned_at=user_ach.earned_at,
            is_displayed=user_ach.is_displayed
        ))
    
    # Collaborative Streaks (user is member of)
    collab_streaks = db.query(CollaborativeStreak).join(CollaborativeStreakMember).filter(
        CollaborativeStreakMember.user_id == current_user.id
    ).order_by(desc(CollaborativeStreak.current_streak)).limit(5).all()
    
    collab_streaks_response = []
    for streak in collab_streaks:
        member_count = db.query(CollaborativeStreakMember).filter(
            CollaborativeStreakMember.streak_id == streak.id
        ).count()
        
        streak_dict = streak.__dict__.copy()
        streak_dict['member_count'] = member_count
        streak_dict['is_member'] = True
        collab_streaks_response.append(CollaborativeStreakResponse(**streak_dict))
    
    # Upcoming Events (next 5)
    upcoming_events = db.query(CommunityEvent).filter(
        CommunityEvent.event_date > datetime.utcnow(),
        CommunityEvent.is_active == True
    ).order_by(CommunityEvent.event_date).limit(5).all()
    
    events_response = []
    for event in upcoming_events:
        attendee_count = db.query(EventAttendee).filter(
            EventAttendee.event_id == event.id
        ).count()
        
        is_attending = db.query(EventAttendee).filter(
            and_(
                EventAttendee.event_id == event.id,
                EventAttendee.user_id == current_user.id
            )
        ).first() is not None
        
        event_dict = event.__dict__.copy()
        event_dict['attendee_count'] = attendee_count
        event_dict['is_attending'] = is_attending
        events_response.append(CommunityEventResponse(**event_dict))
    
    return UserDashboard(
        user_stats=user_stats,
        streak_info=streak_info,
        recent_activities=activities_response,
        achievements=achievements_response,
        collaborative_streaks=collab_streaks_response,
        upcoming_events=events_response
    )

@router.get("/dashboard/stats")
def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get additional dashboard statistics"""
    
    # Weekly activity
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_activities = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id,
        StreakActivity.created_at >= week_ago
    ).all()
    
    # Group by day
    daily_trees = {}
    for activity in weekly_activities:
        day = activity.created_at.strftime("%Y-%m-%d")
        daily_trees[day] = daily_trees.get(day, 0) + activity.trees_count
    
    # Monthly progress
    month_ago = datetime.utcnow() - timedelta(days=30)
    monthly_trees = db.query(func.sum(StreakActivity.trees_count)).filter(
        StreakActivity.user_id == current_user.id,
        StreakActivity.created_at >= month_ago
    ).scalar() or 0
    
    # Rank in community
    users_with_more_trees = db.query(User).filter(
        User.total_trees_planted > current_user.total_trees_planted
    ).count()
    community_rank = users_with_more_trees + 1
    
    # Following stats
    from app.models.social import UserFollow
    followers_count = db.query(UserFollow).filter(
        UserFollow.following_id == current_user.id
    ).count()
    following_count = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id
    ).count()
    
    # Posts stats
    posts_count = db.query(UserPost).filter(
        UserPost.user_id == current_user.id
    ).count()
    
    total_likes = db.query(func.sum(UserPost.likes_count)).filter(
        UserPost.user_id == current_user.id
    ).scalar() or 0
    
    return {
        "weekly_trees": sum(daily_trees.values()),
        "monthly_trees": monthly_trees,
        "daily_breakdown": daily_trees,
        "community_rank": community_rank,
        "social_stats": {
            "followers": followers_count,
            "following": following_count,
            "posts": posts_count,
            "total_likes_received": total_likes
        },
        "streak_stats": {
            "current_streak": current_user.current_streak,
            "longest_streak": current_user.longest_streak,
            "streak_percentage": min(100, (current_user.current_streak / 30) * 100)  # 30-day goal
        }
    }

@router.get("/dashboard/weather")
async def get_weather_info(
    city: str = "Nairobi",
    current_user: User = Depends(get_current_user)
):
    """Get weather information for tree planting using OpenWeather API"""
    from app.services.weather_service import weather_service
    
    # Use user's location if available, otherwise default to Nairobi
    location = current_user.location if current_user.location else city
    
    # Get coordinates for the city
    coordinates = await weather_service.get_coordinates(location)
    if not coordinates:
        # Fallback to Nairobi coordinates
        coordinates = {"lat": -1.2921, "lon": 36.8219}
    
    # Get current weather and forecast
    current_weather = await weather_service.get_current_weather(
        coordinates["lat"], coordinates["lon"]
    )
    forecast = await weather_service.get_forecast(
        coordinates["lat"], coordinates["lon"]
    )
    
    # Get planting advice
    planting_advice = weather_service.get_planting_advice(current_weather, forecast)
    
    return {
        "location": location,
        "coordinates": coordinates,
        "current": current_weather,
        "forecast": forecast,
        "planting_advice": planting_advice,
        "last_updated": datetime.utcnow().isoformat()
    }

@router.get("/dashboard/tips")
def get_daily_tips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized daily tips based on user activity and location"""
    
    # Get user's recent activity to personalize tips
    recent_activities = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id
    ).order_by(desc(StreakActivity.created_at)).limit(5).all()
    
    # Base tips
    tips = [
        {
            "category": "planting",
            "title": "Morning Planting",
            "content": "Plant trees early morning (6-9 AM) when temperatures are cooler and soil moisture is higher.",
            "icon": "🌅"
        },
        {
            "category": "care",
            "title": "Watering Schedule",
            "content": "Water newly planted trees daily for the first month, then reduce to 2-3 times per week.",
            "icon": "💧"
        },
        {
            "category": "species",
            "title": "Native Species",
            "content": "Choose indigenous trees like Mukwa, Meru Oak, or Grevillea for better survival rates in Kenya.",
            "icon": "🌳"
        }
    ]
    
    # Add location-specific tips based on user location
    if current_user.location:
        location_lower = current_user.location.lower()
        if "nairobi" in location_lower or "central" in location_lower:
            tips.append({
                "category": "regional",
                "title": "Central Kenya Tip",
                "content": "In Central Kenya, plant during March-May for best results. Consider Cypress and Pine for higher altitudes.",
                "icon": "🏔️"
            })
        elif "mombasa" in location_lower or "coast" in location_lower:
            tips.append({
                "category": "regional",
                "title": "Coastal Kenya Tip",
                "content": "Coastal areas benefit from Baobab, Coconut palms, and Casuarina trees that tolerate salt spray.",
                "icon": "🏖️"
            })
    
    # Add streak-based tips
    streak = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id
    ).first()
    
    if streak and streak.current_streak > 0:
        tips.append({
            "category": "motivation",
            "title": f"Streak Power! 🔥",
            "content": f"Amazing! You're on a {streak.current_streak}-day streak. Keep it going by logging today's tree activity!",
            "icon": "🔥"
        })
    
    return {"tips": tips[:4]}  # Return max 4 tips
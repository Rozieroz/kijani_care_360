from typing import Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.user import User
from app.models.forum import TreePlantingStreak

router = APIRouter()

@router.get("/dashboard-data")
def get_frontend_analytics_data(
    time_range: str = Query("year", regex="^(month|quarter|year|all)$"),
    county: str = Query("all"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get analytics data in the exact format the frontend expects"""
    
    # Overview statistics
    total_trees = db.query(func.sum(User.total_trees_planted)).scalar() or 0
    total_users = db.query(User).count()
    active_streaks = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.current_streak > 0
    ).count()
    
    overview = {
        "totalTrees": total_trees,
        "forestCoverage": 8.83,  # Kenya's current forest coverage
        "carbonOffset": int(total_trees * 6.5),  # ~6.5kg CO2 per tree
        "activeProjects": 342
    }
    
    # County data for rankings
    county_data = [
        {"name": "Nairobi", "trees": 45678, "coverage": 12.5, "change": 2.3},
        {"name": "Kiambu", "trees": 78234, "coverage": 18.7, "change": 4.1},
        {"name": "Nakuru", "trees": 56789, "coverage": 15.2, "change": 1.8},
        {"name": "Mombasa", "trees": 23456, "coverage": 8.9, "change": 3.2},
        {"name": "Kisumu", "trees": 34567, "coverage": 11.4, "change": 2.7}
    ]
    
    # Monthly planting data
    monthly_planting = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "datasets": [{
            "label": "Trees Planted",
            "data": [12000, 15000, 25000, 35000, 28000, 18000, 15000, 20000, 30000, 40000, 32000, 22000],
            "backgroundColor": "rgba(34, 197, 94, 0.8)",
            "borderColor": "rgba(34, 197, 94, 1)",
            "borderWidth": 2
        }]
    }
    
    # Species distribution
    species_distribution = {
        "labels": ["Indigenous", "Fruit Trees", "Exotic", "Bamboo", "Others"],
        "datasets": [{
            "data": [45, 25, 15, 10, 5],
            "backgroundColor": [
                "rgba(34, 197, 94, 0.8)",
                "rgba(132, 204, 22, 0.8)",
                "rgba(234, 179, 8, 0.8)",
                "rgba(59, 130, 246, 0.8)",
                "rgba(156, 163, 175, 0.8)"
            ],
            "borderWidth": 2
        }]
    }
    
    # Survival rate trends
    survival_rate = {
        "labels": ["2019", "2020", "2021", "2022", "2023", "2024"],
        "datasets": [{
            "label": "Survival Rate (%)",
            "data": [72, 75, 78, 82, 85, 88],
            "borderColor": "rgba(34, 197, 94, 1)",
            "backgroundColor": "rgba(34, 197, 94, 0.1)",
            "tension": 0.4,
            "fill": True
        }]
    }
    
    return {
        "overview": overview,
        "countyData": county_data,
        "monthlyPlanting": monthly_planting,
        "speciesDistribution": species_distribution,
        "survivalRate": survival_rate
    }

@router.get("/community-stats")
def get_community_statistics(db: Session = Depends(get_db)):
    """Get community statistics for the frontend"""
    
    total_users = db.query(User).count()
    total_trees = db.query(func.sum(User.total_trees_planted)).scalar() or 0
    active_streaks = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.current_streak > 0
    ).count()
    
    # Top planters
    top_users = db.query(User).order_by(
        User.total_trees_planted.desc()
    ).limit(5).all()
    
    top_planters = []
    for i, user in enumerate(top_users):
        streak = db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user.id
        ).first()
        
        top_planters.append({
            "user_id": user.id,
            "username": user.username,
            "avatar": user.profile_image,
            "trees_planted": user.total_trees_planted,
            "current_streak": streak.current_streak if streak else 0,
            "points": user.points,
            "rank": i + 1
        })
    
    return {
        "total_users": total_users,
        "total_trees_planted": total_trees,
        "active_streaks": active_streaks,
        "total_events": 25,  # Mock data
        "top_planters": top_planters
    }
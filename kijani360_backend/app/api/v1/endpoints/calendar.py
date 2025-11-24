from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, extract
from datetime import datetime, timedelta, date
from app.database.session import get_db
from app.models.user import User
from app.models.social import CommunityEvent, EventAttendee, StreakActivity
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/events")
def get_calendar_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    month: Optional[int] = None
):
    """Get calendar events for a specific month or all upcoming events"""
    
    if year and month:
        # Get events for specific month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    else:
        # Get upcoming events (next 3 months)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=90)
    
    # Get community events
    community_events = db.query(CommunityEvent).filter(
        and_(
            CommunityEvent.event_date >= start_date,
            CommunityEvent.event_date <= end_date,
            CommunityEvent.is_active == True
        )
    ).all()
    
    # Get user's streak activities as personal events
    user_activities = db.query(StreakActivity).filter(
        and_(
            StreakActivity.user_id == current_user.id,
            StreakActivity.activity_date >= start_date,
            StreakActivity.activity_date <= end_date
        )
    ).all()
    
    # Format events for frontend
    events = []
    
    # Add community events
    for event in community_events:
        events.append({
            "id": f"community_{event.id}",
            "date": event.event_date.isoformat(),
            "type": "community",
            "title": event.title,
            "description": event.description,
            "priority": "high",
            "location": event.location,
            "attendees": db.query(EventAttendee).filter(
                EventAttendee.event_id == event.id
            ).count()
        })
    
    # Add user activities as events
    for activity in user_activities:
        events.append({
            "id": f"activity_{activity.id}",
            "date": activity.activity_date.isoformat(),
            "type": activity.activity_type,
            "title": f"{activity.activity_type.title()} {activity.trees_count} trees",
            "description": activity.description or f"Tree {activity.activity_type} activity",
            "priority": "medium",
            "location": activity.location
        })
    
    # Add seasonal recommendations
    seasonal_events = get_seasonal_recommendations(start_date, end_date, current_user.location)
    events.extend(seasonal_events)
    
    return {"events": events}

@router.post("/events")
def create_calendar_event(
    event_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new calendar event (activity or reminder)"""
    
    if event_data.get("type") == "community":
        # Create community event
        event = CommunityEvent(
            title=event_data["title"],
            description=event_data.get("description", ""),
            event_date=datetime.fromisoformat(event_data["date"]),
            location=event_data.get("location", ""),
            organizer_id=current_user.id,
            tree_planting_goal=event_data.get("tree_goal", 50)
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        
        return {"message": "Community event created", "event_id": event.id}
    
    else:
        # Create personal activity/reminder
        activity = StreakActivity(
            user_id=current_user.id,
            activity_type=event_data.get("type", "reminder"),
            trees_count=event_data.get("trees_count", 1),
            activity_date=datetime.fromisoformat(event_data["date"]),
            location=event_data.get("location"),
            description=event_data.get("description")
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        
        return {"message": "Activity scheduled", "activity_id": activity.id}

@router.get("/recommendations")
def get_planting_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized planting recommendations based on location and season"""
    
    current_month = datetime.now().month
    location = current_user.location or "Kenya"
    
    recommendations = []
    
    # Kenya seasonal recommendations
    if current_month in [3, 4, 5]:  # Long rains (March-May)
        recommendations.extend([
            {
                "title": "🌧️ Long Rains Season - Perfect for Planting!",
                "description": "This is the best time to plant most tree species in Kenya. High survival rates expected.",
                "priority": "high",
                "action": "Plant indigenous trees like Grevillea, Croton, and Markhamia"
            },
            {
                "title": "🌳 Indigenous Species Focus",
                "description": "Plant native species during this season for 80-90% survival rates",
                "priority": "high",
                "action": "Consider Mukwa, Meru Oak, or Prunus africana"
            }
        ])
    
    elif current_month in [10, 11, 12]:  # Short rains (Oct-Dec)
        recommendations.extend([
            {
                "title": "🌦️ Short Rains - Good Planting Window",
                "description": "Second best planting season. Focus on drought-resistant species.",
                "priority": "medium",
                "action": "Plant Melia volkensii, Acacia species, or Terminalia"
            }
        ])
    
    elif current_month in [6, 7, 8, 9]:  # Dry season
        recommendations.extend([
            {
                "title": "☀️ Dry Season - Focus on Care",
                "description": "Not ideal for new planting. Focus on caring for existing trees.",
                "priority": "medium",
                "action": "Water young trees daily, mulch around base, prune dead branches"
            }
        ])
    
    # Location-specific recommendations
    if "central" in location.lower() or "nairobi" in location.lower():
        recommendations.append({
            "title": "🏔️ Central Kenya Advantage",
            "description": "Your highland location is perfect for Grevillea and coffee intercropping",
            "priority": "medium",
            "action": "Consider Grevillea robusta for coffee farms"
        })
    
    elif "eastern" in location.lower() or "machakos" in location.lower() or "kitui" in location.lower():
        recommendations.append({
            "title": "🌵 Dryland Specialist Trees",
            "description": "Your semi-arid location needs drought-resistant species",
            "priority": "high",
            "action": "Focus on Melia volkensii and Acacia species"
        })
    
    elif "coast" in location.lower() or "mombasa" in location.lower():
        recommendations.append({
            "title": "🏖️ Coastal Conditions",
            "description": "Salt-tolerant species work best in your coastal location",
            "priority": "medium",
            "action": "Plant Casuarina for windbreaks and Markhamia for timber"
        })
    
    return {"recommendations": recommendations}

@router.get("/weather-advice")
def get_weather_based_advice():
    """Get weather-based planting and care advice"""
    
    # Mock weather data - in production, integrate with weather API
    current_weather = {
        "temperature": 24,
        "condition": "Partly Cloudy",
        "humidity": 65,
        "rainfall_forecast": "Light rain expected in 2 days"
    }
    
    advice = []
    
    if current_weather["humidity"] > 70:
        advice.append({
            "type": "planting",
            "title": "🌧️ High Humidity - Great for Planting",
            "description": "Current humidity levels are excellent for tree survival",
            "action": "Good day to plant new seedlings"
        })
    
    if "rain" in current_weather["rainfall_forecast"].lower():
        advice.append({
            "type": "care",
            "title": "☔ Rain Coming - Skip Watering",
            "description": "Natural rainfall will provide adequate water",
            "action": "Hold off on watering for 2-3 days after rain"
        })
    
    if current_weather["temperature"] > 30:
        advice.append({
            "type": "care",
            "title": "🌡️ High Temperature - Extra Care Needed",
            "description": "Hot weather increases water stress on young trees",
            "action": "Water early morning or late evening, add mulch"
        })
    
    return {
        "weather": current_weather,
        "advice": advice
    }

def get_seasonal_recommendations(start_date: datetime, end_date: datetime, location: str) -> List[dict]:
    """Generate seasonal planting recommendations for the date range"""
    
    recommendations = []
    current_date = start_date
    
    while current_date <= end_date:
        month = current_date.month
        
        # Add monthly recommendations
        if month in [3, 4, 5] and current_date.day == 1:  # Long rains start
            recommendations.append({
                "id": f"seasonal_{current_date.strftime('%Y%m')}",
                "date": current_date.isoformat(),
                "type": "seasonal",
                "title": "🌧️ Long Rains Season Begins",
                "description": "Optimal time for planting most tree species in Kenya",
                "priority": "high"
            })
        
        elif month in [10, 11, 12] and current_date.day == 1:  # Short rains start
            recommendations.append({
                "id": f"seasonal_{current_date.strftime('%Y%m')}",
                "date": current_date.isoformat(),
                "type": "seasonal",
                "title": "🌦️ Short Rains Season",
                "description": "Good time for drought-resistant species",
                "priority": "medium"
            })
        
        current_date += timedelta(days=30)  # Check monthly
    
    return recommendations
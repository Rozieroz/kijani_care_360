from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.user import User
from app.models.notifications import Notification, NotificationPreference
from app.schemas.notifications import (
    NotificationCreate, Notification as NotificationSchema,
    NotificationPreference as NotificationPreferenceSchema,
    NotificationUpdate, BulkNotificationCreate
)
from app.core.dependencies import get_current_user
from app.services.notification_service import NotificationService

router = APIRouter()

@router.get("/", response_model=List[NotificationSchema])
def get_user_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    unread_only: bool = False,
    limit: int = 50
):
    """Get notifications for current user"""
    query = db.query(Notification).filter(
        Notification.user_id == current_user.id
    )
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(
        desc(Notification.created_at)
    ).limit(limit).all()
    
    return notifications

@router.post("/", response_model=NotificationSchema)
def create_notification(
    notification_data: NotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new notification"""
    notification_service = NotificationService(db)
    notification = notification_service.create_notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        notification_type=notification_data.type,
        data=notification_data.data
    )
    
    # Send push notification in background
    if notification_data.send_push:
        background_tasks.add_task(
            notification_service.send_push_notification,
            notification.id
        )
    
    return notification

@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}

@router.put("/mark-all-read")
def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for current user"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.utcnow()
    })
    db.commit()
    
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return {"message": "Notification deleted"}

@router.get("/preferences", response_model=NotificationPreferenceSchema)
def get_notification_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notification preferences"""
    preferences = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not preferences:
        # Create default preferences
        preferences = NotificationPreference(
            user_id=current_user.id,
            watering_reminders=True,
            forum_replies=True,
            achievement_unlocked=True,
            community_updates=True,
            push_notifications=True,
            email_notifications=True
        )
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
    
    return preferences

@router.put("/preferences", response_model=NotificationPreferenceSchema)
def update_notification_preferences(
    preferences_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's notification preferences"""
    preferences = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id
    ).first()
    
    if not preferences:
        preferences = NotificationPreference(user_id=current_user.id)
        db.add(preferences)
    
    for field, value in preferences_data.items():
        if hasattr(preferences, field):
            setattr(preferences, field, value)
    
    db.commit()
    db.refresh(preferences)
    return preferences

@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    
    return {"unread_count": count}

@router.post("/bulk", response_model=List[NotificationSchema])
def create_bulk_notifications(
    bulk_data: BulkNotificationCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create notifications for multiple users"""
    notification_service = NotificationService(db)
    notifications = []
    
    for user_id in bulk_data.user_ids:
        notification = notification_service.create_notification(
            user_id=user_id,
            title=bulk_data.title,
            message=bulk_data.message,
            notification_type=bulk_data.type,
            data=bulk_data.data
        )
        notifications.append(notification)
        
        # Send push notifications in background
        if bulk_data.send_push:
            background_tasks.add_task(
                notification_service.send_push_notification,
                notification.id
            )
    
    return notifications

@router.post("/watering-reminders")
def schedule_watering_reminders(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Schedule watering reminders for all users with active trees"""
    notification_service = NotificationService(db)
    background_tasks.add_task(
        notification_service.send_watering_reminders
    )
    
    return {"message": "Watering reminders scheduled"}
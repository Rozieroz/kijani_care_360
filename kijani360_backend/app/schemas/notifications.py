from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    WATERING_REMINDER = "watering_reminder"
    FORUM_REPLY = "forum_reply"
    ACHIEVEMENT_UNLOCKED = "achievement_unlocked"
    STREAK_MILESTONE = "streak_milestone"
    COMMUNITY_UPDATE = "community_update"
    SYSTEM_ALERT = "system_alert"

class NotificationBase(BaseModel):
    title: str
    message: str
    type: NotificationType
    data: Optional[Dict[str, Any]] = None

class NotificationCreate(NotificationBase):
    user_id: int
    send_push: bool = True

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None

class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationPreferenceBase(BaseModel):
    watering_reminders: bool = True
    forum_replies: bool = True
    achievement_unlocked: bool = True
    community_updates: bool = True
    push_notifications: bool = True
    email_notifications: bool = True

class NotificationPreference(NotificationPreferenceBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class BulkNotificationCreate(NotificationBase):
    user_ids: List[int]
    send_push: bool = True
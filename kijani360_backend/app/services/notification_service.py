from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.notifications import Notification, NotificationPreference
from app.models.user import User
from app.models.forum import TreePlantingStreak
from app.schemas.notifications import NotificationType

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType,
        data: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type.value,
            data=data
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def send_watering_reminders(self):
        """Send watering reminders to users with active streaks"""
        # Get users with trees that need watering
        active_streaks = self.db.query(TreePlantingStreak).filter(
            TreePlantingStreak.is_active == True,
            TreePlantingStreak.next_watering_date <= datetime.utcnow()
        ).all()
        
        for streak in active_streaks:
            # Check if user wants watering reminders
            preferences = self.db.query(NotificationPreference).filter(
                NotificationPreference.user_id == streak.user_id
            ).first()
            
            if preferences and preferences.watering_reminders:
                self.create_notification(
                    user_id=streak.user_id,
                    title="🌱 Time to Water Your Trees!",
                    message=f"Your {streak.tree_species} needs watering. Keep your streak alive!",
                    notification_type=NotificationType.WATERING_REMINDER,
                    data={
                        "streak_id": streak.id,
                        "tree_species": streak.tree_species,
                        "days_overdue": (datetime.utcnow() - streak.next_watering_date).days
                    }
                )
    
    def send_achievement_notification(
        self,
        user_id: int,
        achievement_name: str,
        achievement_description: str
    ):
        """Send achievement unlocked notification"""
        preferences = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
        
        if preferences and preferences.achievement_unlocked:
            self.create_notification(
                user_id=user_id,
                title="🏆 Achievement Unlocked!",
                message=f"Congratulations! You've earned: {achievement_name}",
                notification_type=NotificationType.ACHIEVEMENT_UNLOCKED,
                data={
                    "achievement_name": achievement_name,
                    "description": achievement_description
                }
            )
    
    def send_streak_milestone_notification(
        self,
        user_id: int,
        streak_days: int,
        tree_species: str
    ):
        """Send streak milestone notification"""
        milestones = [7, 14, 30, 60, 100, 365]
        
        if streak_days in milestones:
            self.create_notification(
                user_id=user_id,
                title=f"🔥 {streak_days} Day Streak!",
                message=f"Amazing! You've maintained your {tree_species} for {streak_days} days straight!",
                notification_type=NotificationType.STREAK_MILESTONE,
                data={
                    "streak_days": streak_days,
                    "tree_species": tree_species,
                    "milestone": True
                }
            )
    
    def send_forum_reply_notification(
        self,
        user_id: int,
        topic_title: str,
        replier_username: str,
        topic_id: int
    ):
        """Send notification when someone replies to user's forum topic"""
        preferences = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == user_id
        ).first()
        
        if preferences and preferences.forum_replies:
            self.create_notification(
                user_id=user_id,
                title="💬 New Reply to Your Topic",
                message=f"{replier_username} replied to '{topic_title}'",
                notification_type=NotificationType.FORUM_REPLY,
                data={
                    "topic_id": topic_id,
                    "topic_title": topic_title,
                    "replier_username": replier_username
                }
            )
    
    def send_community_update(
        self,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None
    ):
        """Send community update to all users who opted in"""
        users_with_preferences = self.db.query(User).join(
            NotificationPreference,
            User.id == NotificationPreference.user_id
        ).filter(
            NotificationPreference.community_updates == True
        ).all()
        
        for user in users_with_preferences:
            self.create_notification(
                user_id=user.id,
                title=title,
                message=message,
                notification_type=NotificationType.COMMUNITY_UPDATE,
                data=data
            )
    
    def send_push_notification(self, notification_id: int):
        """Send push notification (placeholder for actual push service integration)"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not notification:
            return
        
        # Check if user has push notifications enabled
        preferences = self.db.query(NotificationPreference).filter(
            NotificationPreference.user_id == notification.user_id
        ).first()
        
        if preferences and preferences.push_notifications:
            # Here you would integrate with a push notification service
            # like Firebase Cloud Messaging, OneSignal, etc.
            print(f"Sending push notification to user {notification.user_id}: {notification.title}")
    
    def cleanup_old_notifications(self, days_old: int = 30):
        """Clean up old read notifications"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        self.db.query(Notification).filter(
            Notification.is_read == True,
            Notification.read_at < cutoff_date
        ).delete()
        
        self.db.commit()
    
    def get_notification_stats(self, user_id: int) -> Dict[str, int]:
        """Get notification statistics for a user"""
        total = self.db.query(Notification).filter(
            Notification.user_id == user_id
        ).count()
        
        unread = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
        
        return {
            "total_notifications": total,
            "unread_notifications": unread,
            "read_notifications": total - unread
        }
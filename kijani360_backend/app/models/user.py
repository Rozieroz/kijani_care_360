from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    
    # Profile information
    location = Column(String, nullable=True)
    county = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)
    
    # Gamification
    total_trees_planted = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships (commented out to avoid circular imports)
    # notifications = relationship("Notification", back_populates="user")
    # notification_preferences = relationship("NotificationPreference", back_populates="user", uselist=False)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Notification preferences
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    watering_reminders = Column(Boolean, default=True)
    tip_notifications = Column(Boolean, default=True)
    forum_notifications = Column(Boolean, default=True)
    
    # Reminder timing
    reminder_time = Column(String, default="08:00")  # HH:MM format
    timezone = Column(String, default="Africa/Nairobi")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.database.session import Base

# Import existing models to avoid conflicts
from app.models.forum import TreePlantingStreak, Achievement, UserAchievement

class UserFollow(Base):
    """User following system"""
    __tablename__ = "user_follows"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User who follows
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # User being followed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Ensure a user can't follow the same person twice
    __table_args__ = (UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)

# TreePlantingStreak is already defined in forum.py - we'll use that one

class CollaborativeStreak(Base):
    """Collaborative streaks between users - plant trees together!"""
    __tablename__ = "collaborative_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g., "Nairobi Green Warriors"
    description = Column(Text, nullable=True)
    
    # Streak information
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    streak_start_date = Column(DateTime, nullable=True)
    
    # Goals and targets
    daily_tree_goal = Column(Integer, default=5)
    total_trees_planted = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    
    # Creator
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CollaborativeStreakMember(Base):
    """Members of collaborative streaks"""
    __tablename__ = "collaborative_streak_members"
    
    id = Column(Integer, primary_key=True, index=True)
    streak_id = Column(Integer, ForeignKey("collaborative_streaks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Member status
    is_admin = Column(Boolean, default=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_contribution = Column(DateTime, nullable=True)
    
    # Member stats
    trees_contributed = Column(Integer, default=0)
    days_active = Column(Integer, default=0)
    
    # Ensure unique membership
    __table_args__ = (UniqueConstraint('streak_id', 'user_id', name='unique_streak_membership'),)

class StreakActivity(Base):
    """Track daily activities that contribute to streaks"""
    __tablename__ = "streak_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    collaborative_streak_id = Column(Integer, ForeignKey("collaborative_streaks.id"), nullable=True)
    
    # Activity details
    activity_type = Column(String, nullable=False)  # planted, watered, maintained, etc.
    trees_count = Column(Integer, default=1)
    activity_date = Column(DateTime, default=datetime.utcnow)
    
    # Location and context
    location = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_method = Column(String, nullable=True)  # photo, gps, community
    
    # Media
    photo_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UserPost(Base):
    """Social posts for the community feed"""
    __tablename__ = "user_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Post content
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    
    # Post type
    post_type = Column(String, default="general")  # general, achievement, streak, event
    
    # Engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    
    # Visibility
    is_public = Column(Boolean, default=True)
    
    # Tags and location
    tags = Column(String, nullable=True)  # JSON string of tags
    location = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PostLike(Base):
    """Post likes"""
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("user_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Ensure unique likes
    __table_args__ = (UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)

class PostComment(Base):
    """Post comments"""
    __tablename__ = "post_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("user_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    content = Column(Text, nullable=False)
    parent_comment_id = Column(Integer, ForeignKey("post_comments.id"), nullable=True)  # For replies
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Achievement and UserAchievement are already defined in forum.py

class CommunityEvent(Base):
    """Community tree planting events"""
    __tablename__ = "community_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Event details
    event_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    
    # Capacity and goals
    max_attendees = Column(Integer, nullable=True)
    tree_planting_goal = Column(Integer, default=100)
    
    # Organizer
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organizer_name = Column(String, nullable=True)  # For external organizers
    
    # Status
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EventAttendee(Base):
    """Event attendees"""
    __tablename__ = "event_attendees"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("community_events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Attendance status
    status = Column(String, default="registered")  # registered, attended, no_show
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    # Contribution
    trees_planted = Column(Integer, default=0)
    
    # Ensure unique attendance
    __table_args__ = (UniqueConstraint('event_id', 'user_id', name='unique_event_attendance'),)
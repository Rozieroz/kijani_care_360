from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from datetime import datetime
from app.database.session import Base

class ForumCategory(Base):
    __tablename__ = "forum_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    
    # Ordering and visibility
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Stats
    total_posts = Column(Integer, default=0)
    total_topics = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class ForumTopic(Base):
    __tablename__ = "forum_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("forum_categories.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    
    # Topic properties
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Engagement
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)
    
    # Last activity
    last_reply_at = Column(DateTime, nullable=True)
    last_reply_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Tags
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ForumPost(Base):
    __tablename__ = "forum_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("forum_topics.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=True)  # For replies
    
    content = Column(Text, nullable=False)
    
    # Engagement
    likes = Column(Integer, default=0)
    
    # Moderation
    is_deleted = Column(Boolean, default=False)
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime, nullable=True)
    
    # Attachments
    attachments = Column(Text, nullable=True)  # JSON array of file URLs
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ForumLike(Base):
    __tablename__ = "forum_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("forum_topics.id"), nullable=True)
    post_id = Column(Integer, ForeignKey("forum_posts.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class TreePlantingStreak(Base):
    __tablename__ = "tree_planting_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Streak information
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime, nullable=True)
    streak_start_date = Column(DateTime, nullable=True)
    
    # Streak type and status
    streak_type = Column(String, default="daily")  # daily, weekly, monthly
    is_active = Column(Boolean, default=True)
    
    # Legacy fields (keep for compatibility)
    total_trees = Column(Integer, default=0)
    last_planting_date = Column(DateTime, nullable=True)
    achievements = Column(Text, nullable=True)  # JSON array of achievement IDs
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String, nullable=True)
    
    # Achievement criteria (enhanced)
    criteria_type = Column(String, nullable=False)  # trees_planted, streak_days, community_help
    criteria_value = Column(Integer, nullable=False)
    
    # Badge properties (enhanced)
    badge_color = Column(String, default="#22c55e")
    rarity = Column(String, default="common")  # common, rare, epic, legendary
    
    # Points awarded
    points_reward = Column(Integer, default=10)
    
    # Legacy fields (keep for compatibility)
    requirement_type = Column(String, nullable=True)  # Alias for criteria_type
    requirement_value = Column(Integer, nullable=True)  # Alias for criteria_value
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    
    earned_at = Column(DateTime, default=datetime.utcnow)
    is_displayed = Column(Boolean, default=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    
    # Context and metadata
    context = Column(Text, nullable=True)
    confidence_score = Column(String, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    
    # AI model info
    model_used = Column(String, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
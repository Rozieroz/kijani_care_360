from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Forum Category schemas
class ForumCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class ForumCategoryCreate(ForumCategoryBase):
    sort_order: int = 0

class ForumCategory(ForumCategoryBase):
    id: int
    sort_order: int
    is_active: bool
    total_posts: int
    total_topics: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Forum Topic schemas
class ForumTopicBase(BaseModel):
    title: str
    content: str
    category_id: int
    tags: Optional[str] = None

class ForumTopicCreate(ForumTopicBase):
    pass

class ForumTopicUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None

class ForumTopic(ForumTopicBase):
    id: int
    author_id: int
    is_pinned: bool
    is_locked: bool
    is_featured: bool
    views: int
    likes: int
    replies_count: int
    last_reply_at: Optional[datetime]
    last_reply_by: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    # Related data
    category: Optional[ForumCategory] = None
    author_username: Optional[str] = None
    last_reply_username: Optional[str] = None
    
    class Config:
        from_attributes = True

# Forum Post schemas
class ForumPostBase(BaseModel):
    content: str
    parent_post_id: Optional[int] = None

class ForumPostCreate(ForumPostBase):
    topic_id: int

class ForumPostUpdate(BaseModel):
    content: str

class ForumPost(ForumPostBase):
    id: int
    topic_id: int
    author_id: int
    likes: int
    is_deleted: bool
    is_edited: bool
    edited_at: Optional[datetime]
    attachments: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Related data
    author_username: Optional[str] = None
    replies: List['ForumPost'] = []
    
    class Config:
        from_attributes = True

# Update forward reference
ForumPost.model_rebuild()

# Streak and Achievement schemas
class TreePlantingStreakBase(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    total_trees: int = 0

class TreePlantingStreak(TreePlantingStreakBase):
    id: int
    user_id: int
    streak_start_date: Optional[datetime]
    last_planting_date: Optional[datetime]
    achievements: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AchievementBase(BaseModel):
    name: str
    description: str
    icon: Optional[str] = None
    requirement_type: str
    requirement_value: int
    points_reward: int = 0
    badge_color: Optional[str] = None

class AchievementCreate(AchievementBase):
    pass

class Achievement(AchievementBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserAchievement(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    earned_at: datetime
    is_displayed: bool
    
    # Related data
    achievement: Optional[Achievement] = None
    
    class Config:
        from_attributes = True

# Forum interaction schemas
class ForumLikeCreate(BaseModel):
    topic_id: Optional[int] = None
    post_id: Optional[int] = None

class ForumStats(BaseModel):
    total_topics: int
    total_posts: int
    total_users: int
    recent_topics: List[ForumTopic]
    popular_topics: List[ForumTopic]

# Community leaderboard
class CommunityLeaderboard(BaseModel):
    top_planters: List[dict]
    top_contributors: List[dict]
    recent_achievements: List[dict]
    community_stats: dict
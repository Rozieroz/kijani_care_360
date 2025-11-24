from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User Following Schemas
class UserFollowCreate(BaseModel):
    following_id: int

class UserFollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class FollowStats(BaseModel):
    followers_count: int
    following_count: int
    is_following: Optional[bool] = None

# Streak Schemas
class StreakActivityCreate(BaseModel):
    activity_type: str = Field(..., description="Type of activity: planted, watered, maintained")
    trees_count: int = Field(default=1, ge=1)
    location: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    photo_url: Optional[str] = None
    description: Optional[str] = None
    collaborative_streak_id: Optional[int] = None

class StreakActivityResponse(BaseModel):
    id: int
    user_id: int
    activity_type: str
    trees_count: int
    activity_date: datetime
    location: Optional[str]
    is_verified: bool
    photo_url: Optional[str]
    description: Optional[str]
    
    class Config:
        from_attributes = True

class TreePlantingStreakResponse(BaseModel):
    id: int
    user_id: int
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[datetime]
    streak_start_date: Optional[datetime]
    streak_type: str
    is_active: bool
    
    class Config:
        from_attributes = True

# Collaborative Streak Schemas
class CollaborativeStreakCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    daily_tree_goal: int = Field(default=5, ge=1, le=100)
    is_public: bool = True

class CollaborativeStreakResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    current_streak: int
    longest_streak: int
    daily_tree_goal: int
    total_trees_planted: int
    is_active: bool
    is_public: bool
    created_by: int
    member_count: Optional[int] = None
    is_member: Optional[bool] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class CollaborativeStreakMemberResponse(BaseModel):
    id: int
    user_id: int
    username: Optional[str] = None
    is_admin: bool
    joined_at: datetime
    trees_contributed: int
    days_active: int
    
    class Config:
        from_attributes = True

# Post Schemas
class UserPostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    image_url: Optional[str] = None
    post_type: str = Field(default="general")
    tags: Optional[str] = None
    location: Optional[str] = None

class UserPostResponse(BaseModel):
    id: int
    user_id: int
    username: Optional[str] = None
    user_avatar: Optional[str] = None
    content: str
    image_url: Optional[str]
    post_type: str
    likes_count: int
    comments_count: int
    shares_count: int
    tags: Optional[str]
    location: Optional[str]
    is_liked: Optional[bool] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostCommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)
    parent_comment_id: Optional[int] = None

class PostCommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    username: Optional[str] = None
    content: str
    parent_comment_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Achievement Schemas
class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: Optional[str]
    badge_color: str
    rarity: str
    points_reward: int
    
    class Config:
        from_attributes = True

class UserAchievementResponse(BaseModel):
    id: int
    achievement: AchievementResponse
    earned_at: datetime
    is_displayed: bool
    
    class Config:
        from_attributes = True

# Event Schemas
class CommunityEventCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    event_date: datetime
    location: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    max_attendees: Optional[int] = None
    tree_planting_goal: int = Field(default=100, ge=1)
    organizer_name: Optional[str] = None

class CommunityEventResponse(BaseModel):
    id: int
    title: str
    description: str
    event_date: datetime
    location: str
    max_attendees: Optional[int]
    tree_planting_goal: int
    organizer_id: int
    organizer_name: Optional[str]
    attendee_count: Optional[int] = None
    is_attending: Optional[bool] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class UserDashboard(BaseModel):
    user_stats: dict
    streak_info: TreePlantingStreakResponse
    recent_activities: List[StreakActivityResponse]
    achievements: List[UserAchievementResponse]
    collaborative_streaks: List[CollaborativeStreakResponse]
    upcoming_events: List[CommunityEventResponse]

class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    avatar: Optional[str]
    trees_planted: int
    current_streak: int
    points: int
    rank: int

class CommunityStats(BaseModel):
    total_users: int
    total_trees_planted: int
    active_streaks: int
    total_events: int
    top_planters: List[LeaderboardEntry]
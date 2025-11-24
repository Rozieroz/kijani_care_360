from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    location: Optional[str] = None
    county: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    location: Optional[str] = None
    county: Optional[str] = None
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    total_trees_planted: int
    current_streak: int
    longest_streak: int
    points: int
    level: int
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserInDB):
    pass

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# User preferences schemas
class UserPreferencesBase(BaseModel):
    email_notifications: bool = True
    sms_notifications: bool = False
    watering_reminders: bool = True
    tip_notifications: bool = True
    forum_notifications: bool = True
    reminder_time: str = "08:00"
    timezone: str = "Africa/Nairobi"

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(UserPreferencesBase):
    pass

class UserPreferences(UserPreferencesBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# User stats and leaderboard
class UserStats(BaseModel):
    user_id: int
    username: str
    full_name: Optional[str]
    total_trees_planted: int
    current_streak: int
    longest_streak: int
    points: int
    level: int
    rank: Optional[int] = None

class LeaderboardResponse(BaseModel):
    users: List[UserStats]
    user_rank: Optional[int] = None
    total_users: int
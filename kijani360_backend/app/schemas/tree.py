from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Tree Species schemas
class TreeSpeciesBase(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    local_name: Optional[str] = None
    growth_rate: Optional[str] = None
    mature_height: Optional[float] = None
    water_requirements: Optional[str] = None
    soil_type: Optional[str] = None
    climate_zones: Optional[str] = None
    watering_frequency: int = 3

class TreeSpeciesCreate(TreeSpeciesBase):
    pass

class TreeSpecies(TreeSpeciesBase):
    id: int
    timber_value: bool
    fruit_bearing: bool
    medicinal_uses: bool
    erosion_control: bool
    carbon_sequestration: Optional[float]
    survival_rate_coast: Optional[float]
    survival_rate_central: Optional[float]
    survival_rate_western: Optional[float]
    survival_rate_eastern: Optional[float]
    survival_rate_northern: Optional[float]
    survival_rate_rift_valley: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

# User Tree schemas
class UserTreeBase(BaseModel):
    species_id: int
    name: Optional[str] = None
    planting_date: datetime
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class UserTreeCreate(UserTreeBase):
    pass

class UserTreeUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    health_status: Optional[str] = None
    height: Optional[float] = None
    notes: Optional[str] = None

class UserTree(UserTreeBase):
    id: int
    user_id: int
    last_watered: Optional[datetime]
    next_watering_due: Optional[datetime]
    watering_streak: int
    total_waterings: int
    health_status: str
    height: Optional[float]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Related data
    species: Optional[TreeSpecies] = None
    
    class Config:
        from_attributes = True

# Watering Log schemas
class WateringLogBase(BaseModel):
    amount: Optional[float] = None
    method: Optional[str] = None
    notes: Optional[str] = None

class WateringLogCreate(WateringLogBase):
    user_tree_id: int

class WateringLog(WateringLogBase):
    id: int
    user_tree_id: int
    user_id: int
    watered_at: datetime
    temperature: Optional[float]
    humidity: Optional[float]
    rainfall: Optional[float]
    
    class Config:
        from_attributes = True

# Tree Tips schemas
class TreeTipBase(BaseModel):
    title: str
    content: str
    category: str
    species_specific: Optional[int] = None
    season: Optional[str] = None
    region: Optional[str] = None
    difficulty_level: str = "beginner"
    estimated_time: Optional[str] = None

class TreeTipCreate(TreeTipBase):
    author: Optional[str] = None

class TreeTip(TreeTipBase):
    id: int
    author: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Care reminders and calendar
class CareReminder(BaseModel):
    tree_id: int
    tree_name: Optional[str]
    species_name: str
    next_watering_due: datetime
    days_overdue: int
    watering_streak: int
    location: Optional[str]

class CareCalendar(BaseModel):
    user_id: int
    reminders: List[CareReminder]
    total_trees: int
    trees_needing_water: int
    average_streak: float

# Tree care statistics
class TreeCareStats(BaseModel):
    user_id: int
    total_trees: int
    active_trees: int
    total_waterings: int
    average_streak: float
    longest_streak: int
    trees_by_health: dict
    waterings_this_week: int
    waterings_this_month: int
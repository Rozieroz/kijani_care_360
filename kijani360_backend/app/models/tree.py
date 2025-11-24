from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from datetime import datetime
from app.database.session import Base

class TreeSpecies(Base):
    __tablename__ = "tree_species"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=True)
    local_name = Column(String, nullable=True)
    
    # Growing characteristics
    growth_rate = Column(String, nullable=True)  # Fast, Medium, Slow
    mature_height = Column(Float, nullable=True)  # in meters
    water_requirements = Column(String, nullable=True)  # Low, Medium, High
    soil_type = Column(String, nullable=True)
    climate_zones = Column(Text, nullable=True)  # JSON string of suitable zones
    
    # Benefits
    timber_value = Column(Boolean, default=False)
    fruit_bearing = Column(Boolean, default=False)
    medicinal_uses = Column(Boolean, default=False)
    erosion_control = Column(Boolean, default=False)
    carbon_sequestration = Column(Float, nullable=True)  # kg CO2/year
    
    # Care instructions
    watering_frequency = Column(Integer, default=3)  # days
    fertilizer_schedule = Column(Text, nullable=True)
    pruning_schedule = Column(Text, nullable=True)
    
    # Regional data
    survival_rate_coast = Column(Float, nullable=True)
    survival_rate_central = Column(Float, nullable=True)
    survival_rate_western = Column(Float, nullable=True)
    survival_rate_eastern = Column(Float, nullable=True)
    survival_rate_northern = Column(Float, nullable=True)
    survival_rate_rift_valley = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UserTree(Base):
    __tablename__ = "user_trees"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    species_id = Column(Integer, ForeignKey("tree_species.id"), nullable=False)
    
    # Tree details
    name = Column(String, nullable=True)  # User-given name
    planting_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Care tracking
    last_watered = Column(DateTime, nullable=True)
    next_watering_due = Column(DateTime, nullable=True)
    watering_streak = Column(Integer, default=0)
    total_waterings = Column(Integer, default=0)
    
    # Health tracking
    health_status = Column(String, default="healthy")  # healthy, sick, dead
    height = Column(Float, nullable=True)  # current height in cm
    notes = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WateringLog(Base):
    __tablename__ = "watering_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_tree_id = Column(Integer, ForeignKey("user_trees.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    watered_at = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=True)  # liters
    method = Column(String, nullable=True)  # manual, drip, sprinkler
    notes = Column(Text, nullable=True)
    
    # Weather context
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)

class TreeTip(Base):
    __tablename__ = "tree_tips"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # planting, watering, pruning, etc.
    
    # Targeting
    species_specific = Column(Integer, ForeignKey("tree_species.id"), nullable=True)
    season = Column(String, nullable=True)  # dry, wet, all
    region = Column(String, nullable=True)  # coast, central, etc.
    
    # Metadata
    author = Column(String, nullable=True)
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    estimated_time = Column(String, nullable=True)  # "5 minutes", "1 hour"
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
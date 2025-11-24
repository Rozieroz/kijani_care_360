from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class TreeCoverageData(BaseModel):
    year: int
    coverage_percentage: float
    area_hectares: int

class RegionalStats(BaseModel):
    region: str
    coverage_percentage: float
    trees_planted: int
    active_users: int
    recent_plantings: int = 0

class SpeciesPopularity(BaseModel):
    species_name: str
    local_name: str
    planting_count: int
    survival_rate: float

class PlantingTrends(BaseModel):
    period_days: int
    total_plantings: int
    average_daily: float
    daily_data: List[Dict[str, Any]]
    monthly_data: List[Dict[str, Any]]

class UserGrowthStats(BaseModel):
    total_users: int
    active_users: int
    new_users_this_month: int
    users_with_active_streaks: int
    engagement_rate: float

class EnvironmentalImpact(BaseModel):
    total_trees_planted: int
    estimated_co2_absorbed_kg: int
    estimated_oxygen_produced_kg: int
    soil_erosion_prevented_m2: int
    active_conservation_areas: int
    biodiversity_score: float
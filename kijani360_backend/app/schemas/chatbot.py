from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ChatQuery(BaseModel):
    question: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: str = "medium"
    suggestions: Optional[List[str]] = None

class ChatSuggestion(BaseModel):
    text: str
    category: str
    icon: str

class TreeRecommendationRequest(BaseModel):
    region: str
    annual_rainfall: int  # in mm
    farming_system: str  # e.g., "coffee", "maize", "mixed"
    soil_type: Optional[str] = None
    altitude: Optional[int] = None

class TreeRecommendation(BaseModel):
    species_name: str
    local_name: str
    survival_rate: float
    suitability_score: float
    benefits: str
    intercropping: str
    planting_tips: Optional[str] = None
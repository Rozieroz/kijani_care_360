from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.agents.forestry_agent import ForestryAgent
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    region: Optional[str] = None
    soil_type: Optional[str] = None
    rainfall: Optional[str] = None
    context: Optional[Dict] = None

class QueryResponse(BaseModel):
    answer: str
    confidence: float = 0.8
    sources: list = ["Kijani360 Forestry Database", "Kenya Forest Service"]

# Initialize the forestry agent
forestry_agent = ForestryAgent()

@router.post("/query", response_model=QueryResponse)
def query_forestry_agent(
    query: QueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query the RAG-based forestry agent"""
    try:
        # Prepare context
        context = query.context or {}
        if query.region:
            context["region"] = query.region
        if query.soil_type:
            context["soil_type"] = query.soil_type
        if query.rainfall:
            context["rainfall"] = query.rainfall
        
        # Add user location context if available
        if current_user.county and not query.region:
            context["region"] = current_user.county
        
        # Query the agent
        answer = forestry_agent.query(query.question, context)
        
        return QueryResponse(
            answer=answer,
            confidence=0.85,
            sources=[
                "Kijani360 Forestry Database",
                "Kenya Forest Service",
                "ICRAF Agroforestry Database"
            ]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/recommendations")
def get_species_recommendations(
    region: str,
    purpose: str = "general",
    soil_type: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get tree species recommendations based on criteria"""
    try:
        recommendations = forestry_agent.get_species_recommendation(
            region=region,
            purpose=purpose,
            soil_type=soil_type
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.get("/quick-answers")
def get_quick_answers():
    """Get common forestry questions and quick answers"""
    return {
        "common_questions": [
            {
                "question": "What trees grow well in Central Kenya?",
                "category": "regional",
                "quick_answer": "Grevillea robusta, Markhamia lutea, and Croton megalocarpus"
            },
            {
                "question": "Best drought-resistant trees for Eastern Kenya?",
                "category": "drought",
                "quick_answer": "Melia volkensii, Terminalia brownii, and Acacia species"
            },
            {
                "question": "Which trees are good for intercropping with coffee?",
                "category": "agroforestry",
                "quick_answer": "Grevillea robusta, Croton megalocarpus, and shade-tolerant species"
            },
            {
                "question": "What is the survival rate of Grevillea in Rift Valley?",
                "category": "survival_rates",
                "quick_answer": "88% survival rate in Rift Valley region"
            }
        ],
        "categories": [
            "regional_selection",
            "drought_tolerance",
            "agroforestry",
            "survival_rates",
            "intercropping",
            "soil_requirements",
            "planting_timing",
            "care_instructions"
        ]
    }

@router.get("/regions")
def get_kenya_regions():
    """Get information about Kenya's regions for tree planting"""
    return {
        "regions": [
            {
                "name": "Central Kenya",
                "climate": "Temperate, high altitude",
                "rainfall": "High (1000-2000mm)",
                "soil": "Fertile volcanic soils",
                "best_trees": ["Grevillea robusta", "Markhamia lutea", "Croton megalocarpus"]
            },
            {
                "name": "Eastern Kenya",
                "climate": "Semi-arid",
                "rainfall": "Low (300-800mm)",
                "soil": "Sandy, well-drained",
                "best_trees": ["Melia volkensii", "Terminalia brownii", "Acacia species"]
            },
            {
                "name": "Western Kenya",
                "climate": "High rainfall",
                "rainfall": "Very high (1200-2500mm)",
                "soil": "Fertile, well-drained",
                "best_trees": ["Markhamia lutea", "Grevillea robusta", "Indigenous species"]
            },
            {
                "name": "Coast",
                "climate": "Hot, humid",
                "rainfall": "Moderate (800-1200mm)",
                "soil": "Sandy, saline",
                "best_trees": ["Casuarina equisetifolia", "Melia volkensii", "Coconut palm"]
            },
            {
                "name": "Northern Kenya",
                "climate": "Arid",
                "rainfall": "Very low (200-400mm)",
                "soil": "Poor, sandy",
                "best_trees": ["Acacia species", "Prosopis", "Desert date"]
            },
            {
                "name": "Rift Valley",
                "climate": "Varied (arid to temperate)",
                "rainfall": "Variable (400-1500mm)",
                "soil": "Diverse soil types",
                "best_trees": ["Grevillea robusta", "Acacia species", "Markhamia lutea"]
            }
        ]
    }
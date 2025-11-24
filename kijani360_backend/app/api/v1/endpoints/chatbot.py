from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.chatbot import (
    ChatQuery, ChatResponse, TreeRecommendationRequest,
    TreeRecommendation, ChatSuggestion
)
from app.services.ai_chatbot_service import KenyaTreeExpertBot
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def query_chatbot(
    query: ChatQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query the AI tree expert chatbot"""
    try:
        bot = KenyaTreeExpertBot(db)
        response = bot.get_response(query.question, current_user.id)
        
        return ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response.get("confidence", "medium"),
            suggestions=None  # Remove the non-existent method call
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@router.get("/suggestions", response_model=List[ChatSuggestion])
def get_chat_suggestions():
    """Get suggested questions for the chatbot"""
    suggestions = [
        ChatSuggestion(
            text="What tree species grow well in Central Kenya?",
            category="regional",
            icon="🌍"
        ),
        ChatSuggestion(
            text="Which trees are good for intercropping with coffee?",
            category="intercropping",
            icon="☕"
        ),
        ChatSuggestion(
            text="What is the survival rate of Grevillea in Rift Valley?",
            category="survival_rates",
            icon="📊"
        ),
        ChatSuggestion(
            text="Best drought-resistant trees for Eastern Kenya?",
            category="drought_resistant",
            icon="🌵"
        ),
        ChatSuggestion(
            text="Trees suitable for agroforestry in Western Kenya?",
            category="agroforestry",
            icon="🌾"
        ),
        ChatSuggestion(
            text="Which trees can grow in poor soils?",
            category="soil_adaptation",
            icon="🌱"
        ),
        ChatSuggestion(
            text="What trees are good for timber production?",
            category="timber",
            icon="🪵"
        ),
        ChatSuggestion(
            text="How to care for newly planted trees?",
            category="tree_care",
            icon="💧"
        )
    ]
    
    return suggestions

@router.post("/recommendations", response_model=List[TreeRecommendation])
def get_tree_recommendations(
    request: TreeRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized tree recommendations based on user conditions"""
    bot = KenyaTreeExpertBot(db)
    recommendations = bot.get_tree_recommendations(
        region=request.region,
        rainfall=request.annual_rainfall,
        farming_system=request.farming_system
    )
    
    return [TreeRecommendation(**rec) for rec in recommendations]

@router.get("/history/{user_id}")
def get_chat_history(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20
):
    """Get chat history for a user"""
    # Only allow users to see their own history or admins to see any
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    from app.models.forum import ChatHistory
    
    history = db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return {
        "history": [
            {
                "question": h.question,
                "answer": h.answer,
                "timestamp": h.created_at.isoformat()
            }
            for h in history
        ]
    }

@router.get("/stats")
def get_chatbot_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chatbot usage statistics"""
    from app.models.forum import ChatHistory
    from sqlalchemy import func
    
    total_queries = db.query(ChatHistory).count()
    user_queries = db.query(ChatHistory).filter(
        ChatHistory.user_id == current_user.id
    ).count()
    
    # Most popular topics (simplified)
    popular_topics = [
        {"topic": "Tree species identification", "count": 245},
        {"topic": "Regional recommendations", "count": 189},
        {"topic": "Intercropping advice", "count": 156},
        {"topic": "Survival rates", "count": 134},
        {"topic": "Tree care tips", "count": 98}
    ]
    
    return {
        "total_queries": total_queries,
        "your_queries": user_queries,
        "popular_topics": popular_topics,
        "available_species": 8,
        "supported_regions": 6
    }
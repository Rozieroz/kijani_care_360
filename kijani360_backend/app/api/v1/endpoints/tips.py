from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
import random
from app.database.session import get_db
from app.models.tree import TreeTip
from app.schemas.tree import TreeTip as TreeTipSchema

router = APIRouter()

@router.get("/daily", response_model=TreeTipSchema)
def get_daily_tip(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None),
    season: Optional[str] = Query(None)
):
    """Get daily tree growing tip"""
    query = db.query(TreeTip).filter(TreeTip.is_active == True)
    
    # Filter by region if provided
    if region:
        query = query.filter(
            (TreeTip.region == region) | (TreeTip.region.is_(None))
        )
    
    # Filter by season if provided
    if season:
        query = query.filter(
            (TreeTip.season == season) | (TreeTip.season == "all") | (TreeTip.season.is_(None))
        )
    
    tips = query.all()
    
    if not tips:
        # Fallback to any tip
        tips = db.query(TreeTip).filter(TreeTip.is_active == True).all()
    
    if tips:
        # Use date as seed for consistent daily tip
        today = datetime.now().date()
        random.seed(today.toordinal())
        return random.choice(tips)
    
    # Default tip if no tips in database
    return TreeTipSchema(
        id=0,
        title="Welcome to Tree Care!",
        content="Start by planting your first tree and tracking its growth. Remember to water regularly based on your tree species requirements.",
        category="general",
        author="Kijani360 Team",
        difficulty_level="beginner",
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

@router.get("/", response_model=List[TreeTipSchema])
def get_tips(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    species_id: Optional[int] = Query(None),
    limit: int = Query(20, le=100)
):
    """Get tree tips with filters"""
    query = db.query(TreeTip).filter(TreeTip.is_active == True)
    
    if category:
        query = query.filter(TreeTip.category == category)
    
    if difficulty:
        query = query.filter(TreeTip.difficulty_level == difficulty)
    
    if species_id:
        query = query.filter(
            (TreeTip.species_specific == species_id) | (TreeTip.species_specific.is_(None))
        )
    
    return query.limit(limit).all()

@router.get("/categories")
def get_tip_categories(db: Session = Depends(get_db)):
    """Get available tip categories"""
    categories = db.query(TreeTip.category).distinct().all()
    return [cat[0] for cat in categories if cat[0]]

@router.get("/{tip_id}", response_model=TreeTipSchema)
def get_tip(tip_id: int, db: Session = Depends(get_db)):
    """Get specific tip by ID"""
    tip = db.query(TreeTip).filter(
        TreeTip.id == tip_id,
        TreeTip.is_active == True
    ).first()
    
    if not tip:
        raise HTTPException(status_code=404, detail="Tip not found")
    
    return tip
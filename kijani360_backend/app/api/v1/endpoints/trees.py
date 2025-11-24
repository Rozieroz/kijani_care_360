from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.user import User
from app.models.tree import UserTree, TreeSpecies, WateringLog
from app.schemas.tree import (
    UserTreeCreate, UserTree as UserTreeSchema, UserTreeUpdate,
    WateringLogCreate, WateringLog as WateringLogSchema,
    CareCalendar, TreeCareStats, CareReminder
)
from app.core.dependencies import get_current_user
from app.services.tree_care import TreeCareService
from app.services.streak_service import StreakService

router = APIRouter()

@router.post("/plant", response_model=UserTreeSchema)
def plant_tree(
    tree_data: UserTreeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Plant a new tree and start tracking it"""
    # Get species info for watering schedule
    species = db.query(TreeSpecies).filter(TreeSpecies.id == tree_data.species_id).first()
    if not species:
        raise HTTPException(status_code=404, detail="Tree species not found")
    
    # Calculate next watering date
    next_watering = tree_data.planting_date + timedelta(days=species.watering_frequency)
    
    db_tree = UserTree(
        user_id=current_user.id,
        species_id=tree_data.species_id,
        name=tree_data.name,
        planting_date=tree_data.planting_date,
        location=tree_data.location,
        latitude=tree_data.latitude,
        longitude=tree_data.longitude,
        next_watering_due=next_watering
    )
    
    db.add(db_tree)
    
    # Update user stats
    current_user.total_trees_planted += 1
    
    # Update streak
    streak_service = StreakService(db)
    streak_service.update_planting_streak(current_user.id)
    
    db.commit()
    db.refresh(db_tree)
    
    return db_tree

@router.get("/my-trees", response_model=List[UserTreeSchema])
def get_my_trees(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    active_only: bool = Query(True)
):
    """Get user's trees"""
    query = db.query(UserTree).filter(UserTree.user_id == current_user.id)
    if active_only:
        query = query.filter(UserTree.is_active == True)
    
    trees = query.all()
    
    # Add species information
    for tree in trees:
        tree.species = db.query(TreeSpecies).filter(TreeSpecies.id == tree.species_id).first()
    
    return trees

@router.get("/calendar", response_model=CareCalendar)
def get_care_calendar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tree care calendar with reminders"""
    trees = db.query(UserTree).filter(
        UserTree.user_id == current_user.id,
        UserTree.is_active == True
    ).all()
    
    reminders = []
    trees_needing_water = 0
    total_streak = 0
    
    now = datetime.utcnow()
    
    for tree in trees:
        species = db.query(TreeSpecies).filter(TreeSpecies.id == tree.species_id).first()
        days_overdue = 0
        
        if tree.next_watering_due and tree.next_watering_due <= now:
            days_overdue = (now - tree.next_watering_due).days
            trees_needing_water += 1
        
        total_streak += tree.watering_streak
        
        reminder = CareReminder(
            tree_id=tree.id,
            tree_name=tree.name or species.name,
            species_name=species.name,
            next_watering_due=tree.next_watering_due or now,
            days_overdue=days_overdue,
            watering_streak=tree.watering_streak,
            location=tree.location
        )
        reminders.append(reminder)
    
    avg_streak = total_streak / len(trees) if trees else 0
    
    return CareCalendar(
        user_id=current_user.id,
        reminders=reminders,
        total_trees=len(trees),
        trees_needing_water=trees_needing_water,
        average_streak=avg_streak
    )

@router.post("/water/{tree_id}")
def water_tree(
    tree_id: int,
    watering_data: WateringLogCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record watering for a tree"""
    tree = db.query(UserTree).filter(
        UserTree.id == tree_id,
        UserTree.user_id == current_user.id
    ).first()
    
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    
    species = db.query(TreeSpecies).filter(TreeSpecies.id == tree.species_id).first()
    
    # Create watering log
    watering_log = WateringLog(
        user_tree_id=tree.id,
        user_id=current_user.id,
        amount=watering_data.amount,
        method=watering_data.method,
        notes=watering_data.notes
    )
    db.add(watering_log)
    
    # Update tree
    now = datetime.utcnow()
    tree.last_watered = now
    tree.next_watering_due = now + timedelta(days=species.watering_frequency)
    tree.total_waterings += 1
    
    # Update streak
    if tree.last_watered and (now - tree.last_watered).days <= species.watering_frequency + 1:
        tree.watering_streak += 1
    else:
        tree.watering_streak = 1
    
    db.commit()
    
    return {
        "message": "Tree watered successfully",
        "streak": tree.watering_streak,
        "next_watering": tree.next_watering_due
    }

@router.get("/species", response_model=List[dict])
def get_tree_species(
    db: Session = Depends(get_db),
    region: Optional[str] = Query(None)
):
    """Get available tree species with regional data"""
    species = db.query(TreeSpecies).all()
    
    result = []
    for s in species:
        species_data = {
            "id": s.id,
            "name": s.name,
            "scientific_name": s.scientific_name,
            "local_name": s.local_name,
            "growth_rate": s.growth_rate,
            "mature_height": s.mature_height,
            "water_requirements": s.water_requirements,
            "watering_frequency": s.watering_frequency,
            "benefits": {
                "timber_value": s.timber_value,
                "fruit_bearing": s.fruit_bearing,
                "medicinal_uses": s.medicinal_uses,
                "erosion_control": s.erosion_control
            }
        }
        
        # Add regional survival rates
        if region:
            survival_rate = getattr(s, f"survival_rate_{region.lower()}", None)
            species_data["survival_rate"] = survival_rate
        else:
            species_data["regional_survival"] = {
                "coast": s.survival_rate_coast,
                "central": s.survival_rate_central,
                "western": s.survival_rate_western,
                "eastern": s.survival_rate_eastern,
                "northern": s.survival_rate_northern,
                "rift_valley": s.survival_rate_rift_valley
            }
        
        result.append(species_data)
    
    return result

@router.get("/stats", response_model=TreeCareStats)
def get_tree_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's tree care statistics"""
    tree_service = TreeCareService(db)
    return tree_service.get_user_stats(current_user.id)

@router.put("/{tree_id}", response_model=UserTreeSchema)
def update_tree(
    tree_id: int,
    tree_update: UserTreeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update tree information"""
    tree = db.query(UserTree).filter(
        UserTree.id == tree_id,
        UserTree.user_id == current_user.id
    ).first()
    
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    
    update_data = tree_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tree, field, value)
    
    db.commit()
    db.refresh(tree)
    
    return tree

@router.delete("/{tree_id}")
def delete_tree(
    tree_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark tree as inactive (soft delete)"""
    tree = db.query(UserTree).filter(
        UserTree.id == tree_id,
        UserTree.user_id == current_user.id
    ).first()
    
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    
    tree.is_active = False
    db.commit()
    
    return {"message": "Tree removed from tracking"}
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.tree import TreeSpecies, UserTree, WateringLog
from app.models.user import User
from app.models.forum import TreePlantingStreak
from app.schemas.analytics import (
    TreeCoverageData, RegionalStats, SpeciesPopularity,
    PlantingTrends, UserGrowthStats, EnvironmentalImpact
)

router = APIRouter()

# Kenya forest coverage data (historical)
KENYA_COVERAGE_DATA = [
    {"year": 2000, "coverage_percentage": 2.4, "area_hectares": 1392000},
    {"year": 2005, "coverage_percentage": 2.1, "area_hectares": 1218000},
    {"year": 2010, "coverage_percentage": 6.1, "area_hectares": 3537000},
    {"year": 2015, "coverage_percentage": 7.0, "area_hectares": 4060000},
    {"year": 2020, "coverage_percentage": 8.0, "area_hectares": 4640000},
    {"year": 2024, "coverage_percentage": 10.0, "area_hectares": 5800000},
]

@router.get("/tree-coverage", response_model=List[TreeCoverageData])
def get_tree_coverage_data():
    """Get Kenya's historical tree coverage data"""
    return [TreeCoverageData(**data) for data in KENYA_COVERAGE_DATA]

@router.get("/tree-coverage/summary")
def get_coverage_summary():
    """Get tree coverage summary statistics"""
    latest = KENYA_COVERAGE_DATA[-1]
    earliest = KENYA_COVERAGE_DATA[0]
    
    return {
        "current_year": latest["year"],
        "current_coverage": latest["coverage_percentage"],
        "starting_year": earliest["year"],
        "starting_coverage": earliest["coverage_percentage"],
        "improvement": round(latest["coverage_percentage"] - earliest["coverage_percentage"], 2),
        "target": 10.0,
        "progress_to_target": round((latest["coverage_percentage"] / 10.0) * 100, 1)
    }

@router.get("/regional-stats", response_model=List[RegionalStats])
def get_regional_statistics(db: Session = Depends(get_db)):
    """Get tree planting statistics by region"""
    regional_data = [
        {"region": "Central Kenya", "coverage_percentage": 15.2, "trees_planted": 45000, "active_users": 1200},
        {"region": "Western Kenya", "coverage_percentage": 12.8, "trees_planted": 38000, "active_users": 950},
        {"region": "Rift Valley", "coverage_percentage": 8.5, "trees_planted": 52000, "active_users": 1800},
        {"region": "Eastern Kenya", "coverage_percentage": 5.3, "trees_planted": 28000, "active_users": 750},
        {"region": "Coast", "coverage_percentage": 7.1, "trees_planted": 22000, "active_users": 600},
        {"region": "Nyanza", "coverage_percentage": 11.6, "trees_planted": 35000, "active_users": 900},
    ]
    
    # Add real data from database
    for region_data in regional_data:
        # You can add actual database queries here
        region_data["recent_plantings"] = db.query(UserTree).filter(
            UserTree.location.ilike(f"%{region_data['region']}%"),
            UserTree.planting_date >= datetime.now() - timedelta(days=30)
        ).count()
    
    return [RegionalStats(**data) for data in regional_data]

@router.get("/species-popularity", response_model=List[SpeciesPopularity])
def get_species_popularity(
    db: Session = Depends(get_db),
    limit: int = Query(10, le=20)
):
    """Get most popular tree species"""
    species_stats = db.query(
        TreeSpecies.name,
        TreeSpecies.local_name,
        func.count(UserTree.id).label('planting_count'),
        func.avg(TreeSpecies.survival_rate_central).label('avg_survival_rate')
    ).join(
        UserTree, TreeSpecies.id == UserTree.species_id
    ).group_by(
        TreeSpecies.name, TreeSpecies.local_name
    ).order_by(
        func.count(UserTree.id).desc()
    ).limit(limit).all()
    
    return [
        SpeciesPopularity(
            species_name=row.name,
            local_name=row.local_name,
            planting_count=row.planting_count,
            survival_rate=round(row.avg_survival_rate, 2) if row.avg_survival_rate else 0
        )
        for row in species_stats
    ]

@router.get("/planting-trends", response_model=PlantingTrends)
def get_planting_trends(
    db: Session = Depends(get_db),
    days: int = Query(30, ge=7, le=365)
):
    """Get tree planting trends over time"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Daily planting counts
    daily_plantings = db.query(
        func.date(UserTree.planting_date).label('date'),
        func.count(UserTree.id).label('count')
    ).filter(
        UserTree.planting_date >= start_date,
        UserTree.planting_date <= end_date
    ).group_by(
        func.date(UserTree.planting_date)
    ).order_by('date').all()
    
    # Monthly trends
    monthly_plantings = db.query(
        extract('year', UserTree.planting_date).label('year'),
        extract('month', UserTree.planting_date).label('month'),
        func.count(UserTree.id).label('count')
    ).filter(
        UserTree.planting_date >= start_date
    ).group_by(
        extract('year', UserTree.planting_date),
        extract('month', UserTree.planting_date)
    ).order_by('year', 'month').all()
    
    total_plantings = sum(row.count for row in daily_plantings)
    avg_daily = total_plantings / days if days > 0 else 0
    
    return PlantingTrends(
        period_days=days,
        total_plantings=total_plantings,
        average_daily=round(avg_daily, 2),
        daily_data=[
            {"date": str(row.date), "count": row.count}
            for row in daily_plantings
        ],
        monthly_data=[
            {"year": int(row.year), "month": int(row.month), "count": row.count}
            for row in monthly_plantings
        ]
    )

@router.get("/user-growth", response_model=UserGrowthStats)
def get_user_growth_stats(db: Session = Depends(get_db)):
    """Get user growth and engagement statistics"""
    total_users = db.query(User).count()
    
    # Active users (logged in within last 30 days)
    active_users = db.query(User).filter(
        User.last_login >= datetime.now() - timedelta(days=30)
    ).count()
    
    # New users this month
    new_users_month = db.query(User).filter(
        User.created_at >= datetime.now() - timedelta(days=30)
    ).count()
    
    # Users with active streaks
    users_with_streaks = db.query(
        func.count(func.distinct(TreePlantingStreak.user_id))
    ).filter(
        TreePlantingStreak.is_active == True
    ).scalar()
    
    return UserGrowthStats(
        total_users=total_users,
        active_users=active_users,
        new_users_this_month=new_users_month,
        users_with_active_streaks=users_with_streaks or 0,
        engagement_rate=round((active_users / total_users * 100), 2) if total_users > 0 else 0
    )

@router.get("/environmental-impact", response_model=EnvironmentalImpact)
def get_environmental_impact(db: Session = Depends(get_db)):
    """Calculate environmental impact of tree planting activities"""
    total_trees = db.query(UserTree).count()
    
    # Estimates based on average tree impact
    co2_absorbed_kg = total_trees * 22  # Average 22kg CO2 per tree per year
    oxygen_produced_kg = total_trees * 118  # Average 118kg oxygen per tree per year
    soil_erosion_prevented_m2 = total_trees * 15  # Estimated soil protection per tree
    
    # Active conservation areas
    active_areas = db.query(
        func.count(func.distinct(UserTree.location))
    ).scalar()
    
    return EnvironmentalImpact(
        total_trees_planted=total_trees,
        estimated_co2_absorbed_kg=co2_absorbed_kg,
        estimated_oxygen_produced_kg=oxygen_produced_kg,
        soil_erosion_prevented_m2=soil_erosion_prevented_m2,
        active_conservation_areas=active_areas or 0,
        biodiversity_score=min(100, (total_trees / 1000) * 10)  # Simple biodiversity metric
    )

@router.get("/impact-calculator")
def calculate_tree_impact(
    tree_count: int = Query(..., ge=1),
    years: int = Query(1, ge=1, le=50)
):
    """Calculate environmental impact for a given number of trees over time"""
    annual_co2 = tree_count * 22 * years
    annual_oxygen = tree_count * 118 * years
    water_filtered = tree_count * 27000 * years  # Liters per year
    
    return {
        "tree_count": tree_count,
        "years": years,
        "co2_absorbed_kg": annual_co2,
        "oxygen_produced_kg": annual_oxygen,
        "water_filtered_liters": water_filtered,
        "equivalent_cars_offset": round(annual_co2 / 4600, 2),  # Average car emissions
        "people_oxygen_supply": round(annual_oxygen / 550, 0)  # Average person oxygen need
    }
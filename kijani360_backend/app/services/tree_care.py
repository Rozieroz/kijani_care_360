from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.tree import UserTree, WateringLog
from app.schemas.tree import TreeCareStats

class TreeCareService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_stats(self, user_id: int) -> TreeCareStats:
        """Calculate comprehensive tree care statistics for a user"""
        
        # Basic counts
        total_trees = self.db.query(UserTree).filter(UserTree.user_id == user_id).count()
        active_trees = self.db.query(UserTree).filter(
            UserTree.user_id == user_id,
            UserTree.is_active == True
        ).count()
        
        # Total waterings
        total_waterings = self.db.query(WateringLog).filter(
            WateringLog.user_id == user_id
        ).count()
        
        # Streak calculations
        trees = self.db.query(UserTree).filter(
            UserTree.user_id == user_id,
            UserTree.is_active == True
        ).all()
        
        streaks = [tree.watering_streak for tree in trees]
        average_streak = sum(streaks) / len(streaks) if streaks else 0
        longest_streak = max(streaks) if streaks else 0
        
        # Health distribution
        health_counts = self.db.query(
            UserTree.health_status,
            func.count(UserTree.id)
        ).filter(
            UserTree.user_id == user_id,
            UserTree.is_active == True
        ).group_by(UserTree.health_status).all()
        
        trees_by_health = {status: count for status, count in health_counts}
        
        # Recent watering activity
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        waterings_this_week = self.db.query(WateringLog).filter(
            WateringLog.user_id == user_id,
            WateringLog.watered_at >= week_ago
        ).count()
        
        waterings_this_month = self.db.query(WateringLog).filter(
            WateringLog.user_id == user_id,
            WateringLog.watered_at >= month_ago
        ).count()
        
        return TreeCareStats(
            user_id=user_id,
            total_trees=total_trees,
            active_trees=active_trees,
            total_waterings=total_waterings,
            average_streak=round(average_streak, 1),
            longest_streak=longest_streak,
            trees_by_health=trees_by_health,
            waterings_this_week=waterings_this_week,
            waterings_this_month=waterings_this_month
        )
    
    def get_overdue_trees(self, user_id: int):
        """Get trees that need watering"""
        now = datetime.utcnow()
        return self.db.query(UserTree).filter(
            UserTree.user_id == user_id,
            UserTree.is_active == True,
            UserTree.next_watering_due <= now
        ).all()
    
    def calculate_care_score(self, user_id: int) -> float:
        """Calculate a care score based on watering consistency"""
        trees = self.db.query(UserTree).filter(
            UserTree.user_id == user_id,
            UserTree.is_active == True
        ).all()
        
        if not trees:
            return 0.0
        
        total_score = 0
        for tree in trees:
            # Score based on streak and health
            streak_score = min(tree.watering_streak * 10, 100)
            health_multiplier = {"healthy": 1.0, "sick": 0.5, "dead": 0.0}.get(tree.health_status, 0.5)
            tree_score = streak_score * health_multiplier
            total_score += tree_score
        
        return round(total_score / len(trees), 1)
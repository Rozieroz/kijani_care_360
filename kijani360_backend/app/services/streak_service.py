from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.models.forum import TreePlantingStreak

class StreakService:
    def __init__(self, db: Session):
        self.db = db
    
    def update_planting_streak(self, user_id: int):
        """Update user's tree planting streak"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return
        
        # Get or create streak record
        streak = self.db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user_id
        ).first()
        
        if not streak:
            streak = TreePlantingStreak(user_id=user_id)
            self.db.add(streak)
        
        now = datetime.utcnow()
        
        # Check if this continues a streak
        if streak.last_planting_date:
            days_since_last = (now - streak.last_planting_date).days
            
            if days_since_last <= 7:  # Within a week continues streak
                streak.current_streak += 1
            else:
                # Reset streak
                streak.current_streak = 1
                streak.streak_start_date = now
        else:
            # First tree
            streak.current_streak = 1
            streak.streak_start_date = now
        
        # Update records
        streak.last_planting_date = now
        streak.total_trees += 1
        
        # Update longest streak
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        
        # Update user record
        user.current_streak = streak.current_streak
        user.longest_streak = streak.longest_streak
        user.total_trees_planted = streak.total_trees
        
        # Award points
        user.points += 10  # Base points for planting
        if streak.current_streak > 1:
            user.points += streak.current_streak * 2  # Bonus for streaks
        
        # Level up logic
        self._update_user_level(user)
        
        self.db.commit()
    
    def _update_user_level(self, user: User):
        """Update user level based on points"""
        # Simple leveling system
        if user.points >= 1000:
            user.level = 5
        elif user.points >= 500:
            user.level = 4
        elif user.points >= 200:
            user.level = 3
        elif user.points >= 50:
            user.level = 2
        else:
            user.level = 1
    
    def get_leaderboard(self, limit: int = 10):
        """Get top users by current streak"""
        return self.db.query(TreePlantingStreak).order_by(
            TreePlantingStreak.current_streak.desc()
        ).limit(limit).all()
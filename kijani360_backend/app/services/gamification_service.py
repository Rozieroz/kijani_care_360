from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user import User
from app.models.forum import (
    TreePlantingStreak, Achievement, UserAchievement
)
from app.services.notification_service import NotificationService

class GamificationService:
    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)
    
    def check_and_award_achievements(self, user_id: int):
        """Check and award achievements for a user"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return
        
        # Get user's current achievements
        current_achievements = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id
        ).all()
        current_achievement_ids = [ua.achievement_id for ua in current_achievements]
        
        # Check for new achievements
        new_achievements = []
        
        # Tree planting achievements
        total_trees = self.db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user_id
        ).count()
        
        tree_milestones = [
            (1, "First Tree", "Plant your first tree"),
            (5, "Sapling Starter", "Plant 5 trees"),
            (10, "Green Thumb", "Plant 10 trees"),
            (25, "Forest Friend", "Plant 25 trees"),
            (50, "Tree Champion", "Plant 50 trees"),
            (100, "Forest Guardian", "Plant 100 trees")
        ]
        
        for count, name, description in tree_milestones:
            if total_trees >= count:
                achievement = self._get_or_create_achievement(name, description, "tree_planting")
                if achievement.id not in current_achievement_ids:
                    new_achievements.append(achievement)
        
        # Streak achievements
        longest_streak = self._get_longest_streak(user_id)
        streak_milestones = [
            (7, "Week Warrior", "Maintain a 7-day streak"),
            (30, "Monthly Master", "Maintain a 30-day streak"),
            (100, "Streak Legend", "Maintain a 100-day streak"),
            (365, "Year-long Guardian", "Maintain a 365-day streak")
        ]
        
        for days, name, description in streak_milestones:
            if longest_streak >= days:
                achievement = self._get_or_create_achievement(name, description, "streak")
                if achievement.id not in current_achievement_ids:
                    new_achievements.append(achievement)
        
        # Community achievements
        forum_posts = self._get_user_forum_activity(user_id)
        community_milestones = [
            (1, "First Post", "Make your first forum post"),
            (10, "Active Member", "Make 10 forum posts"),
            (50, "Community Leader", "Make 50 forum posts")
        ]
        
        for count, name, description in community_milestones:
            if forum_posts >= count:
                achievement = self._get_or_create_achievement(name, description, "community")
                if achievement.id not in current_achievement_ids:
                    new_achievements.append(achievement)
        
        # Award new achievements
        for achievement in new_achievements:
            self._award_achievement(user_id, achievement)
        
        return new_achievements
    
    def _get_or_create_achievement(self, name: str, description: str, category: str) -> Achievement:
        """Get existing achievement or create new one"""
        achievement = self.db.query(Achievement).filter(
            Achievement.name == name
        ).first()
        
        if not achievement:
            achievement = Achievement(
                name=name,
                description=description,
                category=category,
                icon=self._get_achievement_icon(category),
                points=self._get_achievement_points(name)
            )
            self.db.add(achievement)
            self.db.commit()
            self.db.refresh(achievement)
        
        return achievement
    
    def _award_achievement(self, user_id: int, achievement: Achievement):
        """Award achievement to user"""
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement.id,
            earned_at=datetime.utcnow()
        )
        
        self.db.add(user_achievement)
        self.db.commit()
        
        # Send notification
        self.notification_service.send_achievement_notification(
            user_id=user_id,
            achievement_name=achievement.name,
            achievement_description=achievement.description
        )
        
        # Update user points
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_points = (user.total_points or 0) + achievement.points
            self.db.commit()
    
    def _get_longest_streak(self, user_id: int) -> int:
        """Get user's longest streak"""
        streaks = self.db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user_id
        ).all()
        
        return max([streak.longest_streak for streak in streaks], default=0)
    
    def _get_user_forum_activity(self, user_id: int) -> int:
        """Get user's forum post count"""
        from app.models.forum import ForumPost
        return self.db.query(ForumPost).filter(
            ForumPost.author_id == user_id
        ).count()
    
    def _get_achievement_icon(self, category: str) -> str:
        """Get icon for achievement category"""
        icons = {
            "tree_planting": "🌱",
            "streak": "🔥",
            "community": "👥",
            "environmental": "🌍",
            "knowledge": "🧠"
        }
        return icons.get(category, "🏆")
    
    def _get_achievement_points(self, name: str) -> int:
        """Get points for achievement"""
        point_values = {
            "First Tree": 10,
            "Sapling Starter": 25,
            "Green Thumb": 50,
            "Forest Friend": 100,
            "Tree Champion": 250,
            "Forest Guardian": 500,
            "Week Warrior": 50,
            "Monthly Master": 150,
            "Streak Legend": 500,
            "Year-long Guardian": 1000,
            "First Post": 15,
            "Active Member": 75,
            "Community Leader": 200
        }
        return point_values.get(name, 25)
    
    def get_user_leaderboard_position(self, user_id: int) -> Dict[str, Any]:
        """Get user's position on various leaderboards"""
        from sqlalchemy import func, desc
        
        # Trees planted leaderboard
        tree_ranking = self.db.query(
            User.id,
            func.count(TreePlantingStreak.id).label('tree_count')
        ).join(
            TreePlantingStreak, User.id == TreePlantingStreak.user_id
        ).group_by(User.id).order_by(desc('tree_count')).all()
        
        tree_position = next(
            (i + 1 for i, row in enumerate(tree_ranking) if row.id == user_id),
            None
        )
        
        # Points leaderboard
        points_ranking = self.db.query(User).order_by(
            desc(User.total_points)
        ).all()
        
        points_position = next(
            (i + 1 for i, user in enumerate(points_ranking) if user.id == user_id),
            None
        )
        
        return {
            "tree_planting_rank": tree_position,
            "points_rank": points_position,
            "total_users": len(tree_ranking)
        }
    
    def get_weekly_challenges(self) -> List[Dict[str, Any]]:
        """Get current weekly challenges"""
        # This could be dynamic based on current date, season, etc.
        challenges = [
            {
                "id": 1,
                "title": "Plant Native Species",
                "description": "Plant 3 native Kenyan tree species this week",
                "reward_points": 100,
                "progress_type": "count",
                "target": 3,
                "expires_at": datetime.now() + timedelta(days=7)
            },
            {
                "id": 2,
                "title": "Community Helper",
                "description": "Help 5 community members with tree advice",
                "reward_points": 75,
                "progress_type": "count",
                "target": 5,
                "expires_at": datetime.now() + timedelta(days=7)
            },
            {
                "id": 3,
                "title": "Streak Keeper",
                "description": "Maintain your watering streak for 7 days",
                "reward_points": 150,
                "progress_type": "streak",
                "target": 7,
                "expires_at": datetime.now() + timedelta(days=7)
            }
        ]
        
        return challenges
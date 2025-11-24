from sqlalchemy.orm import Session
from app.models.forum import Achievement
from app.database.session import SessionLocal

def seed_achievements():
    """Seed initial achievements into the database"""
    db = SessionLocal()
    
    achievements_data = [
        # Tree Planting Achievements
        {
            "name": "First Tree Planted",
            "description": "Plant your very first tree and start your conservation journey!",
            "icon": "🌱",
            "criteria_type": "trees_planted",
            "criteria_value": 1,
            "badge_color": "#22c55e",
            "rarity": "common",
            "points_reward": 10
        },
        {
            "name": "Green Thumb",
            "description": "Plant 10 trees and show your commitment to the environment",
            "icon": "🌿",
            "criteria_type": "trees_planted",
            "criteria_value": 10,
            "badge_color": "#16a34a",
            "rarity": "common",
            "points_reward": 25
        },
        {
            "name": "Tree Warrior",
            "description": "Plant 50 trees and become a true environmental warrior!",
            "icon": "🌳",
            "criteria_type": "trees_planted",
            "criteria_value": 50,
            "badge_color": "#15803d",
            "rarity": "rare",
            "points_reward": 100
        },
        {
            "name": "Forest Guardian",
            "description": "Plant 100 trees and join the ranks of forest guardians",
            "icon": "🏆",
            "criteria_type": "trees_planted",
            "criteria_value": 100,
            "badge_color": "#166534",
            "rarity": "epic",
            "points_reward": 250
        },
        {
            "name": "Reforestation Hero",
            "description": "Plant 500 trees and become a true reforestation hero!",
            "icon": "👑",
            "criteria_type": "trees_planted",
            "criteria_value": 500,
            "badge_color": "#14532d",
            "rarity": "legendary",
            "points_reward": 1000
        },
        
        # Streak Achievements
        {
            "name": "Getting Started",
            "description": "Maintain a 3-day planting streak",
            "icon": "🔥",
            "criteria_type": "streak_days",
            "criteria_value": 3,
            "badge_color": "#f59e0b",
            "rarity": "common",
            "points_reward": 15
        },
        {
            "name": "Consistency Champion",
            "description": "Maintain a 7-day planting streak",
            "icon": "⚡",
            "criteria_type": "streak_days",
            "criteria_value": 7,
            "badge_color": "#d97706",
            "rarity": "common",
            "points_reward": 35
        },
        {
            "name": "Dedication Master",
            "description": "Maintain a 30-day planting streak",
            "icon": "💪",
            "criteria_type": "streak_days",
            "criteria_value": 30,
            "badge_color": "#c2410c",
            "rarity": "rare",
            "points_reward": 150
        },
        {
            "name": "Streak Legend",
            "description": "Maintain a 100-day planting streak",
            "icon": "🌟",
            "criteria_type": "streak_days",
            "criteria_value": 100,
            "badge_color": "#9a3412",
            "rarity": "epic",
            "points_reward": 500
        },
        {
            "name": "Unstoppable Force",
            "description": "Maintain a 365-day planting streak",
            "icon": "💎",
            "criteria_type": "streak_days",
            "criteria_value": 365,
            "badge_color": "#7c2d12",
            "rarity": "legendary",
            "points_reward": 2000
        },
        
        # Community Achievements
        {
            "name": "Community Helper",
            "description": "Help 10 community members with their tree planting",
            "icon": "🤝",
            "criteria_type": "community_help",
            "criteria_value": 10,
            "badge_color": "#3b82f6",
            "rarity": "rare",
            "points_reward": 75
        },
        {
            "name": "Mentor",
            "description": "Guide 25 new tree planters in the community",
            "icon": "🎓",
            "criteria_type": "community_help",
            "criteria_value": 25,
            "badge_color": "#2563eb",
            "rarity": "epic",
            "points_reward": 200
        },
        
        # Special Achievements
        {
            "name": "Early Adopter",
            "description": "One of the first 100 users to join KijaniCare360",
            "icon": "🚀",
            "criteria_type": "early_adopter",
            "criteria_value": 100,
            "badge_color": "#8b5cf6",
            "rarity": "legendary",
            "points_reward": 500
        },
        {
            "name": "Photo Documenter",
            "description": "Share 20 photos of your planted trees",
            "icon": "📸",
            "criteria_type": "photos_shared",
            "criteria_value": 20,
            "badge_color": "#ec4899",
            "rarity": "rare",
            "points_reward": 100
        },
        {
            "name": "Location Explorer",
            "description": "Plant trees in 5 different locations",
            "icon": "🗺️",
            "criteria_type": "locations_planted",
            "criteria_value": 5,
            "badge_color": "#06b6d4",
            "rarity": "rare",
            "points_reward": 125
        }
    ]
    
    try:
        # Check if achievements already exist
        existing_count = db.query(Achievement).count()
        if existing_count > 0:
            print(f"Achievements already exist ({existing_count} found). Skipping seed.")
            return
        
        # Create achievements
        for ach_data in achievements_data:
            achievement = Achievement(**ach_data)
            db.add(achievement)
        
        db.commit()
        print(f"Successfully seeded {len(achievements_data)} achievements!")
        
    except Exception as e:
        print(f"Error seeding achievements: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_achievements()
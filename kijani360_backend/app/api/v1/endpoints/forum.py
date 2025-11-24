from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database.session import get_db
from app.models.user import User
from app.models.forum import (
    ForumCategory, ForumTopic, ForumPost, ForumLike, 
    TreePlantingStreak, Achievement, UserAchievement
)
from app.schemas.forum import (
    ForumCategoryCreate, ForumCategory as ForumCategorySchema,
    ForumTopicCreate, ForumTopic as ForumTopicSchema, ForumTopicUpdate,
    ForumPostCreate, ForumPost as ForumPostSchema, ForumPostUpdate,
    ForumLikeCreate, TreePlantingStreak as TreePlantingStreakSchema,
    Achievement as AchievementSchema, UserAchievement as UserAchievementSchema,
    ForumStats, CommunityLeaderboard
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

# Categories
@router.get("/categories", response_model=List[ForumCategorySchema])
def get_categories(db: Session = Depends(get_db)):
    """Get all forum categories"""
    return db.query(ForumCategory).filter(
        ForumCategory.is_active == True
    ).order_by(ForumCategory.sort_order).all()

@router.post("/categories", response_model=ForumCategorySchema)
def create_category(
    category_data: ForumCategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new forum category (admin only)"""
    db_category = ForumCategory(**category_data.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Topics
@router.get("/topics", response_model=List[ForumTopicSchema])
def get_topics(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None),
    featured_only: bool = Query(False),
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):
    """Get forum topics with filters"""
    query = db.query(ForumTopic)
    
    if category_id:
        query = query.filter(ForumTopic.category_id == category_id)
    
    if featured_only:
        query = query.filter(ForumTopic.is_featured == True)
    
    topics = query.order_by(
        desc(ForumTopic.is_pinned),
        desc(ForumTopic.last_reply_at)
    ).offset(offset).limit(limit).all()
    
    # Add related data
    for topic in topics:
        topic.category = db.query(ForumCategory).filter(
            ForumCategory.id == topic.category_id
        ).first()
        
        author = db.query(User).filter(User.id == topic.author_id).first()
        topic.author_username = author.username if author else "Unknown"
        
        if topic.last_reply_by:
            last_replier = db.query(User).filter(User.id == topic.last_reply_by).first()
            topic.last_reply_username = last_replier.username if last_replier else "Unknown"
    
    return topics

@router.post("/topics", response_model=ForumTopicSchema)
def create_topic(
    topic_data: ForumTopicCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new forum topic"""
    db_topic = ForumTopic(
        **topic_data.dict(),
        author_id=current_user.id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@router.get("/topics/{topic_id}", response_model=ForumTopicSchema)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get a specific topic with posts"""
    topic = db.query(ForumTopic).filter(ForumTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Increment view count
    topic.view_count += 1
    db.commit()
    
    return topic

@router.put("/topics/{topic_id}", response_model=ForumTopicSchema)
def update_topic(
    topic_id: int,
    topic_data: ForumTopicUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a topic (author or admin only)"""
    topic = db.query(ForumTopic).filter(ForumTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    if topic.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in topic_data.dict(exclude_unset=True).items():
        setattr(topic, field, value)
    
    db.commit()
    db.refresh(topic)
    return topic

# Posts
@router.get("/topics/{topic_id}/posts", response_model=List[ForumPostSchema])
def get_topic_posts(
    topic_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):
    """Get posts for a specific topic"""
    posts = db.query(ForumPost).filter(
        ForumPost.topic_id == topic_id
    ).order_by(ForumPost.created_at).offset(offset).limit(limit).all()
    
    # Add author info
    for post in posts:
        author = db.query(User).filter(User.id == post.author_id).first()
        post.author_username = author.username if author else "Unknown"
        post.author_avatar = author.avatar_url if author else None
    
    return posts

@router.post("/topics/{topic_id}/posts", response_model=ForumPostSchema)
def create_post(
    topic_id: int,
    post_data: ForumPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new post in a topic"""
    topic = db.query(ForumTopic).filter(ForumTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    db_post = ForumPost(
        **post_data.dict(),
        topic_id=topic_id,
        author_id=current_user.id
    )
    db.add(db_post)
    
    # Update topic stats
    topic.reply_count += 1
    topic.last_reply_at = db_post.created_at
    topic.last_reply_by = current_user.id
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.put("/posts/{post_id}", response_model=ForumPostSchema)
def update_post(
    post_id: int,
    post_data: ForumPostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a post (author or admin only)"""
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in post_data.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    return post

# Likes
@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like or unlike a post"""
    existing_like = db.query(ForumLike).filter(
        ForumLike.post_id == post_id,
        ForumLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        liked = False
    else:
        # Like
        db_like = ForumLike(post_id=post_id, user_id=current_user.id)
        db.add(db_like)
        liked = True
    
    # Update post like count
    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if post:
        like_count = db.query(ForumLike).filter(ForumLike.post_id == post_id).count()
        post.like_count = like_count
    
    db.commit()
    return {"liked": liked, "like_count": post.like_count if post else 0}

# Tree Planting Streaks
@router.get("/streaks", response_model=List[TreePlantingStreakSchema])
def get_user_streaks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's tree planting streaks"""
    return db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id,
        TreePlantingStreak.is_active == True
    ).all()

@router.post("/streaks", response_model=TreePlantingStreakSchema)
def create_streak(
    streak_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new tree planting streak"""
    db_streak = TreePlantingStreak(
        user_id=current_user.id,
        tree_species=streak_data.get("tree_species"),
        location=streak_data.get("location"),
        target_count=streak_data.get("target_count", 1)
    )
    db.add(db_streak)
    db.commit()
    db.refresh(db_streak)
    return db_streak

# Achievements
@router.get("/achievements", response_model=List[AchievementSchema])
def get_achievements(db: Session = Depends(get_db)):
    """Get all available achievements"""
    return db.query(Achievement).filter(Achievement.is_active == True).all()

@router.get("/users/{user_id}/achievements", response_model=List[UserAchievementSchema])
def get_user_achievements(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get achievements for a specific user"""
    return db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).all()

# Community Stats
@router.get("/stats", response_model=ForumStats)
def get_forum_stats(db: Session = Depends(get_db)):
    """Get forum statistics"""
    total_topics = db.query(ForumTopic).count()
    total_posts = db.query(ForumPost).count()
    total_users = db.query(User).count()
    active_streaks = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.is_active == True
    ).count()
    
    return ForumStats(
        total_topics=total_topics,
        total_posts=total_posts,
        total_users=total_users,
        active_streaks=active_streaks
    )

@router.get("/leaderboard", response_model=List[CommunityLeaderboard])
def get_community_leaderboard(
    db: Session = Depends(get_db),
    limit: int = Query(10, le=50)
):
    """Get community leaderboard based on tree planting activity"""
    leaderboard = db.query(
        User.id,
        User.username,
        User.avatar_url,
        func.sum(TreePlantingStreak.current_count).label('total_trees'),
        func.count(TreePlantingStreak.id).label('streak_count')
    ).join(
        TreePlantingStreak, User.id == TreePlantingStreak.user_id
    ).group_by(
        User.id, User.username, User.avatar_url
    ).order_by(
        desc('total_trees')
    ).limit(limit).all()
    
    return [
        CommunityLeaderboard(
            user_id=row.id,
            username=row.username,
            avatar_url=row.avatar_url,
            total_trees=row.total_trees or 0,
            streak_count=row.streak_count or 0
        )
        for row in leaderboard
    ]
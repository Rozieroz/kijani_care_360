from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_
from datetime import datetime, timedelta
from app.database.session import get_db
from app.models.user import User
from app.models.social import (
    UserPost, PostLike, PostComment, UserFollow,
    CommunityEvent, EventAttendee, CollaborativeStreak, CollaborativeStreakMember
)
from app.core.dependencies import get_current_user

router = APIRouter()

@router.get("/feed")
def get_community_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0)
):
    """Get community feed with posts from followed users and public posts"""
    
    # Get posts from followed users and public posts
    followed_users_subquery = db.query(UserFollow.following_id).filter(
        UserFollow.follower_id == current_user.id
    ).subquery()
    
    posts_query = db.query(UserPost, User.username, User.profile_image).join(
        User, UserPost.user_id == User.id
    ).filter(
        or_(
            UserPost.user_id.in_(followed_users_subquery),
            UserPost.is_public == True,
            UserPost.user_id == current_user.id  # Include user's own posts
        )
    ).order_by(desc(UserPost.created_at))
    
    posts = posts_query.offset(offset).limit(limit).all()
    
    result = []
    for post, username, profile_image in posts:
        # Check if current user liked this post
        is_liked = db.query(PostLike).filter(
            and_(
                PostLike.post_id == post.id,
                PostLike.user_id == current_user.id
            )
        ).first() is not None
        
        result.append({
            "id": post.id,
            "user_id": post.user_id,
            "username": username,
            "user_avatar": profile_image,
            "content": post.content,
            "image_url": post.image_url,
            "post_type": post.post_type,
            "likes_count": post.likes_count,
            "comments_count": post.comments_count,
            "shares_count": post.shares_count,
            "tags": post.tags,
            "location": post.location,
            "is_liked": is_liked,
            "created_at": post.created_at.isoformat()
        })
    
    return result

@router.post("/posts")
def create_post(
    post_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new community post"""
    
    post = UserPost(
        user_id=current_user.id,
        content=post_data["content"],
        image_url=post_data.get("image_url"),
        post_type=post_data.get("post_type", "general"),
        tags=post_data.get("tags"),
        location=post_data.get("location"),
        is_public=post_data.get("is_public", True)
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return {
        "id": post.id,
        "message": "Post created successfully",
        "post": {
            "id": post.id,
            "content": post.content,
            "created_at": post.created_at.isoformat()
        }
    }

@router.post("/posts/{post_id}/like")
def toggle_post_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like or unlike a post"""
    
    post = db.query(UserPost).filter(UserPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(PostLike).filter(
        and_(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        )
    ).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.likes_count = max(0, post.likes_count - 1)
        action = "unliked"
    else:
        # Like
        like = PostLike(post_id=post_id, user_id=current_user.id)
        db.add(like)
        post.likes_count += 1
        action = "liked"
    
    db.commit()
    
    return {
        "action": action,
        "likes_count": post.likes_count,
        "is_liked": action == "liked"
    }

@router.get("/events")
def get_community_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    upcoming_only: bool = Query(True)
):
    """Get community events"""
    
    query = db.query(CommunityEvent)
    
    if upcoming_only:
        query = query.filter(CommunityEvent.event_date >= datetime.utcnow())
    
    events = query.filter(
        CommunityEvent.is_active == True
    ).order_by(CommunityEvent.event_date).all()
    
    result = []
    for event in events:
        attendee_count = db.query(EventAttendee).filter(
            EventAttendee.event_id == event.id
        ).count()
        
        is_attending = db.query(EventAttendee).filter(
            and_(
                EventAttendee.event_id == event.id,
                EventAttendee.user_id == current_user.id
            )
        ).first() is not None
        
        result.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "event_date": event.event_date.isoformat(),
            "location": event.location,
            "max_attendees": event.max_attendees,
            "tree_planting_goal": event.tree_planting_goal,
            "organizer_id": event.organizer_id,
            "organizer_name": event.organizer_name,
            "attendee_count": attendee_count,
            "is_attending": is_attending,
            "created_at": event.created_at.isoformat()
        })
    
    return result

@router.post("/events/{event_id}/join")
def join_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a community event"""
    
    event = db.query(CommunityEvent).filter(CommunityEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if already attending
    existing_attendance = db.query(EventAttendee).filter(
        and_(
            EventAttendee.event_id == event_id,
            EventAttendee.user_id == current_user.id
        )
    ).first()
    
    if existing_attendance:
        raise HTTPException(status_code=400, detail="Already registered for this event")
    
    # Check capacity
    if event.max_attendees:
        current_attendees = db.query(EventAttendee).filter(
            EventAttendee.event_id == event_id
        ).count()
        if current_attendees >= event.max_attendees:
            raise HTTPException(status_code=400, detail="Event is full")
    
    # Add attendance
    attendance = EventAttendee(
        event_id=event_id,
        user_id=current_user.id,
        status="registered"
    )
    db.add(attendance)
    db.commit()
    
    return {"message": "Successfully joined event"}

@router.get("/leaderboard")
def get_community_leaderboard(
    db: Session = Depends(get_db),
    metric: str = Query("trees", regex="^(trees|streak|points)$"),
    limit: int = Query(10, le=50)
):
    """Get community leaderboard"""
    
    if metric == "trees":
        users = db.query(User).order_by(desc(User.total_trees_planted)).limit(limit).all()
        
        result = []
        for i, user in enumerate(users):
            result.append({
                "rank": i + 1,
                "user_id": user.id,
                "username": user.username,
                "avatar": user.profile_image,
                "trees_planted": user.total_trees_planted,
                "current_streak": user.current_streak,
                "points": user.points,
                "location": user.location
            })
        
        return result
    
    elif metric == "points":
        users = db.query(User).order_by(desc(User.points)).limit(limit).all()
        
        result = []
        for i, user in enumerate(users):
            result.append({
                "rank": i + 1,
                "user_id": user.id,
                "username": user.username,
                "avatar": user.profile_image,
                "trees_planted": user.total_trees_planted,
                "current_streak": user.current_streak,
                "points": user.points,
                "location": user.location
            })
        
        return result
    
    else:  # streak
        users = db.query(User).order_by(desc(User.current_streak)).limit(limit).all()
        
        result = []
        for i, user in enumerate(users):
            result.append({
                "rank": i + 1,
                "user_id": user.id,
                "username": user.username,
                "avatar": user.profile_image,
                "trees_planted": user.total_trees_planted,
                "current_streak": user.current_streak,
                "points": user.points,
                "location": user.location
            })
        
        return result

@router.get("/stats")
def get_community_stats(db: Session = Depends(get_db)):
    """Get overall community statistics"""
    
    total_users = db.query(User).count()
    total_trees = db.query(func.sum(User.total_trees_planted)).scalar() or 0
    total_posts = db.query(UserPost).count()
    active_events = db.query(CommunityEvent).filter(
        and_(
            CommunityEvent.event_date >= datetime.utcnow(),
            CommunityEvent.is_active == True
        )
    ).count()
    
    # Active users (posted or logged activity in last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_users = db.query(func.count(func.distinct(User.id))).filter(
        or_(
            User.last_login >= thirty_days_ago,
            User.id.in_(
                db.query(UserPost.user_id).filter(UserPost.created_at >= thirty_days_ago)
            )
        )
    ).scalar() or 0
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_trees_planted": total_trees,
        "total_posts": total_posts,
        "active_events": active_events,
        "engagement_rate": round((active_users / total_users * 100), 1) if total_users > 0 else 0
    }

@router.get("/trending-topics")
def get_trending_topics(db: Session = Depends(get_db)):
    """Get trending hashtags and topics"""
    
    # Mock trending topics - in production, analyze post tags
    trending = [
        {"topic": "#TreePlanting", "count": 245, "growth": "+15%"},
        {"topic": "#IndigenousTrees", "count": 189, "growth": "+8%"},
        {"topic": "#UrbanForestry", "count": 156, "growth": "+22%"},
        {"topic": "#ClimateAction", "count": 134, "growth": "+12%"},
        {"topic": "#KenyaForests", "count": 98, "growth": "+5%"},
        {"topic": "#Agroforestry", "count": 87, "growth": "+18%"},
        {"topic": "#CommunityPlanting", "count": 76, "growth": "+25%"}
    ]
    
    return {"trending_topics": trending}

@router.get("/suggested-users")
def get_suggested_users(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(5, le=20)
):
    """Get suggested users to follow"""
    
    # Get users current user is not following
    following_subquery = db.query(UserFollow.following_id).filter(
        UserFollow.follower_id == current_user.id
    ).subquery()
    
    suggested_users = db.query(User).filter(
        and_(
            User.id != current_user.id,
            ~User.id.in_(following_subquery),
            User.total_trees_planted > 0  # Users who have planted trees
        )
    ).order_by(desc(User.total_trees_planted)).limit(limit).all()
    
    result = []
    for user in suggested_users:
        # Get follower count
        followers_count = db.query(UserFollow).filter(
            UserFollow.following_id == user.id
        ).count()
        
        result.append({
            "user_id": user.id,
            "username": user.username,
            "avatar": user.profile_image,
            "location": user.location,
            "trees_planted": user.total_trees_planted,
            "followers_count": followers_count,
            "reason": "Active tree planter" if user.total_trees_planted > 10 else "New member"
        })
    
    return {"suggested_users": result}
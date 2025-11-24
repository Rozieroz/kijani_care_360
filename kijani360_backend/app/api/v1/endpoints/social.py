from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_
from datetime import datetime, timedelta, date

from app.database.session import get_db
from app.models.user import User
from app.models.social import (
    UserFollow, CollaborativeStreak, CollaborativeStreakMember,
    StreakActivity, UserPost, PostLike, PostComment,
    CommunityEvent, EventAttendee
)
from app.models.forum import TreePlantingStreak, Achievement, UserAchievement
from app.schemas.social import (
    UserFollowCreate, UserFollowResponse, FollowStats,
    StreakActivityCreate, StreakActivityResponse, TreePlantingStreakResponse,
    CollaborativeStreakCreate, CollaborativeStreakResponse, CollaborativeStreakMemberResponse,
    UserPostCreate, UserPostResponse, PostCommentCreate, PostCommentResponse,
    AchievementResponse, UserAchievementResponse,
    CommunityEventCreate, CommunityEventResponse,
    UserDashboard, LeaderboardEntry, CommunityStats
)
from app.core.dependencies import get_current_user

router = APIRouter()

# ============ FOLLOWING SYSTEM ============

@router.post("/follow", response_model=UserFollowResponse)
def follow_user(
    follow_data: UserFollowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow another user"""
    # Check if user exists
    target_user = db.query(User).filter(User.id == follow_data.following_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Can't follow yourself
    if follow_data.following_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Check if already following
    existing_follow = db.query(UserFollow).filter(
        and_(
            UserFollow.follower_id == current_user.id,
            UserFollow.following_id == follow_data.following_id
        )
    ).first()
    
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")
    
    # Create follow relationship
    follow = UserFollow(
        follower_id=current_user.id,
        following_id=follow_data.following_id
    )
    db.add(follow)
    db.commit()
    db.refresh(follow)
    
    return follow

@router.delete("/unfollow/{user_id}")
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow a user"""
    follow = db.query(UserFollow).filter(
        and_(
            UserFollow.follower_id == current_user.id,
            UserFollow.following_id == user_id
        )
    ).first()
    
    if not follow:
        raise HTTPException(status_code=404, detail="Not following this user")
    
    db.delete(follow)
    db.commit()
    
    return {"message": "Successfully unfollowed user"}

@router.get("/follow-stats/{user_id}", response_model=FollowStats)
def get_follow_stats(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get follow statistics for a user"""
    followers_count = db.query(UserFollow).filter(UserFollow.following_id == user_id).count()
    following_count = db.query(UserFollow).filter(UserFollow.follower_id == user_id).count()
    
    # Check if current user is following this user
    is_following = None
    if current_user.id != user_id:
        is_following = db.query(UserFollow).filter(
            and_(
                UserFollow.follower_id == current_user.id,
                UserFollow.following_id == user_id
            )
        ).first() is not None
    
    return FollowStats(
        followers_count=followers_count,
        following_count=following_count,
        is_following=is_following
    )

# ============ STREAK SYSTEM ============

@router.post("/streak/activity", response_model=StreakActivityResponse)
def log_streak_activity(
    activity: StreakActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a tree planting activity to maintain streak"""
    # Create activity record
    streak_activity = StreakActivity(
        user_id=current_user.id,
        activity_type=activity.activity_type,
        trees_count=activity.trees_count,
        location=activity.location,
        latitude=activity.latitude,
        longitude=activity.longitude,
        photo_url=activity.photo_url,
        description=activity.description,
        collaborative_streak_id=activity.collaborative_streak_id
    )
    db.add(streak_activity)
    
    # Update or create user streak
    user_streak = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id
    ).first()
    
    if not user_streak:
        user_streak = TreePlantingStreak(user_id=current_user.id)
        db.add(user_streak)
    
    # Update streak logic
    today = datetime.utcnow().date()
    last_activity = user_streak.last_activity_date.date() if user_streak.last_activity_date else None
    
    if last_activity == today:
        # Already logged today, just update trees count
        pass
    elif last_activity == today - timedelta(days=1):
        # Consecutive day, increment streak
        user_streak.current_streak += 1
        user_streak.longest_streak = max(user_streak.longest_streak, user_streak.current_streak)
    elif last_activity is None or last_activity < today - timedelta(days=1):
        # Streak broken or first activity, reset to 1
        user_streak.current_streak = 1
        user_streak.streak_start_date = datetime.utcnow()
    
    user_streak.last_activity_date = datetime.utcnow()
    
    # Update user total trees
    current_user.total_trees_planted += activity.trees_count
    
    # Update collaborative streak if applicable
    if activity.collaborative_streak_id:
        collab_streak = db.query(CollaborativeStreak).filter(
            CollaborativeStreak.id == activity.collaborative_streak_id
        ).first()
        if collab_streak:
            collab_streak.total_trees_planted += activity.trees_count
            
            # Update member contribution
            member = db.query(CollaborativeStreakMember).filter(
                and_(
                    CollaborativeStreakMember.streak_id == activity.collaborative_streak_id,
                    CollaborativeStreakMember.user_id == current_user.id
                )
            ).first()
            if member:
                member.trees_contributed += activity.trees_count
                member.last_contribution = datetime.utcnow()
    
    db.commit()
    db.refresh(streak_activity)
    
    # Check for achievements
    _check_achievements(current_user, db)
    
    return streak_activity

@router.get("/streak/my", response_model=TreePlantingStreakResponse)
def get_my_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's streak information"""
    streak = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.user_id == current_user.id
    ).first()
    
    if not streak:
        # Create initial streak record
        streak = TreePlantingStreak(user_id=current_user.id)
        db.add(streak)
        db.commit()
        db.refresh(streak)
    
    return streak

@router.get("/streak/activities", response_model=List[StreakActivityResponse])
def get_my_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100)
):
    """Get user's recent activities"""
    activities = db.query(StreakActivity).filter(
        StreakActivity.user_id == current_user.id
    ).order_by(desc(StreakActivity.created_at)).limit(limit).all()
    
    return activities

# ============ COLLABORATIVE STREAKS ============

@router.post("/collaborative-streak", response_model=CollaborativeStreakResponse)
def create_collaborative_streak(
    streak_data: CollaborativeStreakCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new collaborative streak"""
    collab_streak = CollaborativeStreak(
        name=streak_data.name,
        description=streak_data.description,
        daily_tree_goal=streak_data.daily_tree_goal,
        is_public=streak_data.is_public,
        created_by=current_user.id,
        streak_start_date=datetime.utcnow()
    )
    db.add(collab_streak)
    db.commit()
    db.refresh(collab_streak)
    
    # Add creator as admin member
    member = CollaborativeStreakMember(
        streak_id=collab_streak.id,
        user_id=current_user.id,
        is_admin=True
    )
    db.add(member)
    db.commit()
    
    return collab_streak

@router.post("/collaborative-streak/{streak_id}/join")
def join_collaborative_streak(
    streak_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a collaborative streak"""
    # Check if streak exists
    streak = db.query(CollaborativeStreak).filter(
        CollaborativeStreak.id == streak_id
    ).first()
    if not streak:
        raise HTTPException(status_code=404, detail="Streak not found")
    
    # Check if already a member
    existing_member = db.query(CollaborativeStreakMember).filter(
        and_(
            CollaborativeStreakMember.streak_id == streak_id,
            CollaborativeStreakMember.user_id == current_user.id
        )
    ).first()
    
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member of this streak")
    
    # Add as member
    member = CollaborativeStreakMember(
        streak_id=streak_id,
        user_id=current_user.id
    )
    db.add(member)
    db.commit()
    
    return {"message": "Successfully joined collaborative streak"}

@router.get("/collaborative-streaks", response_model=List[CollaborativeStreakResponse])
def get_collaborative_streaks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    my_streaks: bool = Query(False),
    limit: int = Query(20, le=100)
):
    """Get collaborative streaks"""
    query = db.query(CollaborativeStreak)
    
    if my_streaks:
        # Get streaks user is a member of
        query = query.join(CollaborativeStreakMember).filter(
            CollaborativeStreakMember.user_id == current_user.id
        )
    else:
        # Get public streaks
        query = query.filter(CollaborativeStreak.is_public == True)
    
    streaks = query.order_by(desc(CollaborativeStreak.created_at)).limit(limit).all()
    
    # Add member count and membership status
    result = []
    for streak in streaks:
        member_count = db.query(CollaborativeStreakMember).filter(
            CollaborativeStreakMember.streak_id == streak.id
        ).count()
        
        is_member = db.query(CollaborativeStreakMember).filter(
            and_(
                CollaborativeStreakMember.streak_id == streak.id,
                CollaborativeStreakMember.user_id == current_user.id
            )
        ).first() is not None
        
        streak_dict = streak.__dict__.copy()
        streak_dict['member_count'] = member_count
        streak_dict['is_member'] = is_member
        result.append(CollaborativeStreakResponse(**streak_dict))
    
    return result

# ============ SOCIAL POSTS ============

@router.post("/posts", response_model=UserPostResponse)
def create_post(
    post_data: UserPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new social post"""
    post = UserPost(
        user_id=current_user.id,
        content=post_data.content,
        image_url=post_data.image_url,
        post_type=post_data.post_type,
        tags=post_data.tags,
        location=post_data.location
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    
    # Add username for response
    post_dict = post.__dict__.copy()
    post_dict['username'] = current_user.username
    post_dict['is_liked'] = False
    
    return UserPostResponse(**post_dict)

@router.get("/posts/feed", response_model=List[UserPostResponse])
def get_community_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0)
):
    """Get community feed posts"""
    # Get posts from followed users and public posts
    followed_users = db.query(UserFollow.following_id).filter(
        UserFollow.follower_id == current_user.id
    ).subquery()
    
    posts = db.query(UserPost, User.username).join(User).filter(
        or_(
            UserPost.user_id.in_(followed_users),
            UserPost.is_public == True
        )
    ).order_by(desc(UserPost.created_at)).offset(offset).limit(limit).all()
    
    result = []
    for post, username in posts:
        # Check if current user liked this post
        is_liked = db.query(PostLike).filter(
            and_(
                PostLike.post_id == post.id,
                PostLike.user_id == current_user.id
            )
        ).first() is not None
        
        post_dict = post.__dict__.copy()
        post_dict['username'] = username
        post_dict['is_liked'] = is_liked
        result.append(UserPostResponse(**post_dict))
    
    return result

@router.post("/posts/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Like or unlike a post"""
    # Check if post exists
    post = db.query(UserPost).filter(UserPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
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
    return {"message": f"Post {action} successfully", "likes_count": post.likes_count}

@router.get("/posts/my-posts", response_model=List[UserPostResponse])
def get_my_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100)
):
    """Get current user's posts"""
    posts = db.query(UserPost).filter(
        UserPost.user_id == current_user.id
    ).order_by(desc(UserPost.created_at)).limit(limit).all()
    
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        post_dict['username'] = current_user.username
        post_dict['is_liked'] = False  # User can't like own posts
        result.append(UserPostResponse(**post_dict))
    
    return result

@router.get("/streak/collaborative")
def get_my_collaborative_streaks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's collaborative streak data"""
    # Get user's collaborative streaks
    member_streaks = db.query(CollaborativeStreak, CollaborativeStreakMember).join(
        CollaborativeStreakMember
    ).filter(
        CollaborativeStreakMember.user_id == current_user.id
    ).first()
    
    if not member_streaks:
        return {
            "group_streak": 0,
            "group_members": [],
            "group_name": "",
            "individual_contribution": 0,
            "group_goal": 30,
            "last_group_activity": None,
            "is_group_active": False,
            "group_id": None
        }
    
    streak, membership = member_streaks
    
    # Get all members
    members = db.query(CollaborativeStreakMember, User.username).join(User).filter(
        CollaborativeStreakMember.streak_id == streak.id
    ).all()
    
    member_list = []
    for member, username in members:
        member_list.append({
            "id": member.user_id,
            "name": username if member.user_id != current_user.id else "You",
            "avatar": "👤",
            "contribution": member.trees_contributed,
            "last_activity": member.last_contribution.strftime("%H hours ago") if member.last_contribution else "No activity"
        })
    
    return {
        "group_streak": streak.current_streak_days,
        "group_members": member_list,
        "group_name": streak.name,
        "individual_contribution": membership.trees_contributed,
        "group_goal": streak.daily_tree_goal * 30,  # Monthly goal
        "last_group_activity": streak.last_activity_date.isoformat() if streak.last_activity_date else None,
        "is_group_active": streak.is_active,
        "group_id": streak.id
    }

@router.post("/streak/groups/{group_id}/invite-link")
def generate_invite_link(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate invite link for streak group"""
    # Verify user is member of the group
    membership = db.query(CollaborativeStreakMember).filter(
        and_(
            CollaborativeStreakMember.streak_id == group_id,
            CollaborativeStreakMember.user_id == current_user.id
        )
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    return {"invite_link": f"https://kijanicare360.com/join-streak/{group_id}"}

@router.post("/streak/groups/{group_id}/invite-emails")
def send_email_invites(
    group_id: int,
    emails_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send email invitations to join streak group"""
    # Verify user is member of the group
    membership = db.query(CollaborativeStreakMember).filter(
        and_(
            CollaborativeStreakMember.streak_id == group_id,
            CollaborativeStreakMember.user_id == current_user.id
        )
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this group")
    
    emails = emails_data.get("emails", [])
    # In production, send actual emails here
    return {"message": f"Invitations sent to {len(emails)} recipients"}

@router.get("/messages/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's message conversations"""
    # Mock data for now - in production, implement actual messaging
    return []

@router.get("/messages/conversations/{conversation_id}")
def get_conversation_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages in a conversation"""
    # Mock data for now - in production, implement actual messaging
    return []

@router.post("/messages")
def send_message(
    message_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a new message"""
    # Mock response for now - in production, implement actual messaging
    return {"id": 1, "message": "Message sent successfully"}

# ============ LEADERBOARD & STATS ============

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(
    db: Session = Depends(get_db),
    limit: int = Query(10, le=50),
    metric: str = Query("trees", regex="^(trees|streak|points)$")
):
    """Get community leaderboard"""
    if metric == "trees":
        order_by = desc(User.total_trees_planted)
        value_field = "total_trees_planted"
    elif metric == "streak":
        # Join with streak table
        users = db.query(
            User, TreePlantingStreak.current_streak
        ).outerjoin(TreePlantingStreak).order_by(
            desc(TreePlantingStreak.current_streak)
        ).limit(limit).all()
        
        result = []
        for i, (user, streak) in enumerate(users):
            result.append(LeaderboardEntry(
                user_id=user.id,
                username=user.username,
                avatar=user.profile_image,
                trees_planted=user.total_trees_planted,
                current_streak=streak or 0,
                points=user.points,
                rank=i + 1
            ))
        return result
    else:  # points
        order_by = desc(User.points)
        value_field = "points"
    
    users = db.query(User).order_by(order_by).limit(limit).all()
    
    result = []
    for i, user in enumerate(users):
        # Get user's streak
        streak = db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user.id
        ).first()
        
        result.append(LeaderboardEntry(
            user_id=user.id,
            username=user.username,
            avatar=user.profile_image,
            trees_planted=user.total_trees_planted,
            current_streak=streak.current_streak if streak else 0,
            points=user.points,
            rank=i + 1
        ))
    
    return result

@router.get("/stats/community", response_model=CommunityStats)
def get_community_stats(db: Session = Depends(get_db)):
    """Get overall community statistics"""
    total_users = db.query(User).count()
    total_trees = db.query(func.sum(User.total_trees_planted)).scalar() or 0
    active_streaks = db.query(TreePlantingStreak).filter(
        TreePlantingStreak.current_streak > 0
    ).count()
    total_events = db.query(CommunityEvent).count()
    
    # Top 5 planters
    top_users = db.query(User).order_by(
        desc(User.total_trees_planted)
    ).limit(5).all()
    
    top_planters = []
    for i, user in enumerate(top_users):
        streak = db.query(TreePlantingStreak).filter(
            TreePlantingStreak.user_id == user.id
        ).first()
        
        top_planters.append(LeaderboardEntry(
            user_id=user.id,
            username=user.username,
            avatar=user.profile_image,
            trees_planted=user.total_trees_planted,
            current_streak=streak.current_streak if streak else 0,
            points=user.points,
            rank=i + 1
        ))
    
    return CommunityStats(
        total_users=total_users,
        total_trees_planted=total_trees,
        active_streaks=active_streaks,
        total_events=total_events,
        top_planters=top_planters
    )

# ============ HELPER FUNCTIONS ============

def _check_achievements(user: User, db: Session):
    """Check and award achievements to user"""
    # Get all achievements user hasn't earned yet
    earned_achievement_ids = db.query(UserAchievement.achievement_id).filter(
        UserAchievement.user_id == user.id
    ).subquery()
    
    available_achievements = db.query(Achievement).filter(
        ~Achievement.id.in_(earned_achievement_ids)
    ).all()
    
    for achievement in available_achievements:
        earned = False
        
        if achievement.criteria_type == "trees_planted":
            earned = user.total_trees_planted >= achievement.criteria_value
        elif achievement.criteria_type == "streak_days":
            streak = db.query(TreePlantingStreak).filter(
                TreePlantingStreak.user_id == user.id
            ).first()
            earned = streak and streak.longest_streak >= achievement.criteria_value
        
        if earned:
            # Award achievement
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id
            )
            db.add(user_achievement)
            
            # Award points
            user.points += achievement.points_reward
    
    db.commit()
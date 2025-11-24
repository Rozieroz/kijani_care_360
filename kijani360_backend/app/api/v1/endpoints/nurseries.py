from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.nursery import Nursery, SeedlingListing, Order, OrderItem, NurseryReview
from app.schemas.nursery import (
    NurseryCreate, Nursery as NurserySchema, NurseryUpdate,
    SeedlingListingCreate, SeedlingListing as SeedlingListingSchema,
    OrderCreate, Order as OrderSchema,
    NurseryReviewCreate, NurseryReview as NurseryReviewSchema,
    NurserySearchFilters, SeedlingSearchResponse
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.post("/register", response_model=NurserySchema)
def register_nursery(
    nursery_data: NurseryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register a new nursery"""
    db_nursery = Nursery(
        owner_id=current_user.id,
        **nursery_data.dict()
    )
    db.add(db_nursery)
    db.commit()
    db.refresh(db_nursery)
    return db_nursery

@router.get("/", response_model=List[NurserySchema])
def get_nurseries(
    db: Session = Depends(get_db),
    county: Optional[str] = Query(None),
    verified_only: bool = Query(False),
    limit: int = Query(20, le=100)
):
    """Get list of nurseries with filters"""
    query = db.query(Nursery).filter(Nursery.is_active == True)
    
    if county:
        query = query.filter(Nursery.county.ilike(f"%{county}%"))
    
    if verified_only:
        query = query.filter(Nursery.is_verified == True)
    
    return query.limit(limit).all()

@router.get("/{nursery_id}", response_model=NurserySchema)
def get_nursery(nursery_id: int, db: Session = Depends(get_db)):
    """Get nursery details"""
    nursery = db.query(Nursery).filter(
        Nursery.id == nursery_id,
        Nursery.is_active == True
    ).first()
    
    if not nursery:
        raise HTTPException(status_code=404, detail="Nursery not found")
    
    return nursery

@router.put("/{nursery_id}", response_model=NurserySchema)
def update_nursery(
    nursery_id: int,
    nursery_update: NurseryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update nursery information"""
    nursery = db.query(Nursery).filter(
        Nursery.id == nursery_id,
        Nursery.owner_id == current_user.id
    ).first()
    
    if not nursery:
        raise HTTPException(status_code=404, detail="Nursery not found or not owned by user")
    
    update_data = nursery_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(nursery, field, value)
    
    db.commit()
    db.refresh(nursery)
    return nursery

@router.post("/{nursery_id}/listings", response_model=SeedlingListingSchema)
def create_seedling_listing(
    nursery_id: int,
    listing_data: SeedlingListingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new seedling listing"""
    # Verify nursery ownership
    nursery = db.query(Nursery).filter(
        Nursery.id == nursery_id,
        Nursery.owner_id == current_user.id
    ).first()
    
    if not nursery:
        raise HTTPException(status_code=404, detail="Nursery not found or not owned by user")
    
    db_listing = SeedlingListing(
        nursery_id=nursery_id,
        **listing_data.dict()
    )
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing

@router.get("/search/seedlings", response_model=SeedlingSearchResponse)
def search_seedlings(
    db: Session = Depends(get_db),
    county: Optional[str] = Query(None),
    species_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    delivery_available: Optional[bool] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, le=100)
):
    """Search seedling listings"""
    query = db.query(SeedlingListing).join(Nursery).filter(
        SeedlingListing.is_available == True,
        Nursery.is_active == True
    )
    
    if county:
        query = query.filter(Nursery.county.ilike(f"%{county}%"))
    
    if species_id:
        query = query.filter(SeedlingListing.species_id == species_id)
    
    if min_price:
        query = query.filter(SeedlingListing.price >= min_price)
    
    if max_price:
        query = query.filter(SeedlingListing.price <= max_price)
    
    if delivery_available is not None:
        query = query.filter(SeedlingListing.delivery_available == delivery_available)
    
    # Get total count
    total_count = query.count()
    
    # Apply pagination
    offset = (page - 1) * per_page
    listings = query.offset(offset).limit(per_page).all()
    
    # Add nursery information
    for listing in listings:
        listing.nursery = db.query(Nursery).filter(Nursery.id == listing.nursery_id).first()
    
    total_pages = (total_count + per_page - 1) // per_page
    
    return SeedlingSearchResponse(
        listings=listings,
        total_count=total_count,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.post("/orders", response_model=OrderSchema)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new order"""
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item_data in order_data.items:
        listing = db.query(SeedlingListing).filter(
            SeedlingListing.id == item_data.listing_id,
            SeedlingListing.is_available == True
        ).first()
        
        if not listing:
            raise HTTPException(status_code=404, detail=f"Listing {item_data.listing_id} not found")
        
        if item_data.quantity > listing.quantity_available:
            raise HTTPException(status_code=400, detail=f"Insufficient quantity for listing {item_data.listing_id}")
        
        item_total = listing.price * item_data.quantity
        total_amount += item_total
        
        order_items.append({
            "listing_id": item_data.listing_id,
            "quantity": item_data.quantity,
            "unit_price": listing.price,
            "total_price": item_total
        })
    
    # Create order
    import uuid
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    
    db_order = Order(
        buyer_id=current_user.id,
        nursery_id=order_data.nursery_id,
        order_number=order_number,
        total_amount=total_amount,
        delivery_address=order_data.delivery_address,
        delivery_phone=order_data.delivery_phone,
        buyer_notes=order_data.buyer_notes
    )
    db.add(db_order)
    db.flush()  # Get order ID
    
    # Create order items
    for item_data in order_items:
        db_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    
    # Load related data
    db_order.items = db.query(OrderItem).filter(OrderItem.order_id == db_order.id).all()
    db_order.nursery = db.query(Nursery).filter(Nursery.id == db_order.nursery_id).first()
    
    return db_order

@router.get("/my-orders", response_model=List[OrderSchema])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's orders"""
    orders = db.query(Order).filter(Order.buyer_id == current_user.id).all()
    
    for order in orders:
        order.items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
        order.nursery = db.query(Nursery).filter(Nursery.id == order.nursery_id).first()
    
    return orders

@router.post("/{nursery_id}/reviews", response_model=NurseryReviewSchema)
def create_nursery_review(
    nursery_id: int,
    review_data: NurseryReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a nursery review"""
    # Check if nursery exists
    nursery = db.query(Nursery).filter(Nursery.id == nursery_id).first()
    if not nursery:
        raise HTTPException(status_code=404, detail="Nursery not found")
    
    # Check if user already reviewed this nursery
    existing_review = db.query(NurseryReview).filter(
        NurseryReview.nursery_id == nursery_id,
        NurseryReview.reviewer_id == current_user.id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this nursery")
    
    db_review = NurseryReview(
        nursery_id=nursery_id,
        reviewer_id=current_user.id,
        **review_data.dict(exclude={"nursery_id"})
    )
    db.add(db_review)
    
    # Update nursery rating
    reviews = db.query(NurseryReview).filter(NurseryReview.nursery_id == nursery_id).all()
    total_rating = sum(r.rating for r in reviews) + review_data.rating
    total_reviews = len(reviews) + 1
    
    nursery.average_rating = total_rating / total_reviews
    nursery.total_reviews = total_reviews
    
    db.commit()
    db.refresh(db_review)
    
    return db_review
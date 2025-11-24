from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Nursery schemas
class NurseryBase(BaseModel):
    name: str
    description: Optional[str] = None
    phone_number: str
    email: Optional[EmailStr] = None
    county: str
    town: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class NurseryCreate(NurseryBase):
    established_year: Optional[int] = None
    license_number: Optional[str] = None
    certification: Optional[str] = None

class NurseryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    town: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class Nursery(NurseryBase):
    id: int
    owner_id: int
    established_year: Optional[int]
    license_number: Optional[str]
    certification: Optional[str]
    average_rating: float
    total_reviews: int
    total_sales: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Seedling Listing schemas
class SeedlingListingBase(BaseModel):
    species_id: int
    title: str
    description: Optional[str] = None
    price: float
    quantity_available: int
    minimum_order: int = 1
    age_months: Optional[int] = None
    height_cm: Optional[float] = None
    pot_size: Optional[str] = None

class SeedlingListingCreate(SeedlingListingBase):
    delivery_available: bool = False
    delivery_cost: Optional[float] = None
    delivery_radius_km: Optional[int] = None
    seasonal_availability: Optional[str] = None

class SeedlingListingUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    quantity_available: Optional[int] = None
    minimum_order: Optional[int] = None
    is_available: Optional[bool] = None
    delivery_available: Optional[bool] = None
    delivery_cost: Optional[float] = None

class SeedlingListing(SeedlingListingBase):
    id: int
    nursery_id: int
    primary_image: Optional[str]
    additional_images: Optional[str]
    is_available: bool
    seasonal_availability: Optional[str]
    delivery_available: bool
    delivery_cost: Optional[float]
    delivery_radius_km: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    # Related data
    nursery: Optional[Nursery] = None
    
    class Config:
        from_attributes = True

# Order schemas
class OrderItemCreate(BaseModel):
    listing_id: int
    quantity: int

class OrderCreate(BaseModel):
    nursery_id: int
    items: List[OrderItemCreate]
    delivery_address: Optional[str] = None
    delivery_phone: Optional[str] = None
    buyer_notes: Optional[str] = None

class OrderItem(BaseModel):
    id: int
    listing_id: int
    quantity: int
    unit_price: float
    total_price: float
    
    # Related data
    listing: Optional[SeedlingListing] = None
    
    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    buyer_id: int
    nursery_id: int
    order_number: str
    total_amount: float
    delivery_cost: float
    status: str
    payment_status: str
    delivery_address: Optional[str]
    delivery_phone: Optional[str]
    estimated_delivery: Optional[datetime]
    actual_delivery: Optional[datetime]
    buyer_notes: Optional[str]
    nursery_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    # Related data
    items: List[OrderItem] = []
    nursery: Optional[Nursery] = None
    
    class Config:
        from_attributes = True

# Review schemas
class NurseryReviewBase(BaseModel):
    rating: int  # 1-5
    title: Optional[str] = None
    comment: Optional[str] = None
    seedling_quality: Optional[int] = None
    delivery_speed: Optional[int] = None
    customer_service: Optional[int] = None

class NurseryReviewCreate(NurseryReviewBase):
    nursery_id: int
    order_id: Optional[int] = None

class NurseryReview(NurseryReviewBase):
    id: int
    nursery_id: int
    reviewer_id: int
    order_id: Optional[int]
    is_verified_purchase: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Search and filter schemas
class NurserySearchFilters(BaseModel):
    county: Optional[str] = None
    species_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    delivery_available: Optional[bool] = None
    min_rating: Optional[float] = None
    verified_only: Optional[bool] = None

class SeedlingSearchResponse(BaseModel):
    listings: List[SeedlingListing]
    total_count: int
    page: int
    per_page: int
    total_pages: int
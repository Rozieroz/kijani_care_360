from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey
from datetime import datetime
from app.database.session import Base

class Nursery(Base):
    __tablename__ = "nurseries"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Basic information
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    
    # Location
    county = Column(String, nullable=False)
    town = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Business details
    established_year = Column(Integer, nullable=True)
    license_number = Column(String, nullable=True)
    certification = Column(String, nullable=True)
    
    # Ratings and reviews
    average_rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    total_sales = Column(Integer, default=0)
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SeedlingListing(Base):
    __tablename__ = "seedling_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    nursery_id = Column(Integer, ForeignKey("nurseries.id"), nullable=False)
    species_id = Column(Integer, ForeignKey("tree_species.id"), nullable=False)
    
    # Listing details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)  # KES
    quantity_available = Column(Integer, nullable=False)
    minimum_order = Column(Integer, default=1)
    
    # Seedling details
    age_months = Column(Integer, nullable=True)
    height_cm = Column(Float, nullable=True)
    pot_size = Column(String, nullable=True)
    
    # Images
    primary_image = Column(String, nullable=True)
    additional_images = Column(Text, nullable=True)  # JSON array of image URLs
    
    # Availability
    is_available = Column(Boolean, default=True)
    seasonal_availability = Column(String, nullable=True)
    
    # Delivery
    delivery_available = Column(Boolean, default=False)
    delivery_cost = Column(Float, nullable=True)
    delivery_radius_km = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nursery_id = Column(Integer, ForeignKey("nurseries.id"), nullable=False)
    
    # Order details
    order_number = Column(String, unique=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    delivery_cost = Column(Float, default=0.0)
    
    # Status
    status = Column(String, default="pending")  # pending, confirmed, shipped, delivered, cancelled
    payment_status = Column(String, default="pending")  # pending, paid, failed, refunded
    
    # Delivery
    delivery_address = Column(Text, nullable=True)
    delivery_phone = Column(String, nullable=True)
    estimated_delivery = Column(DateTime, nullable=True)
    actual_delivery = Column(DateTime, nullable=True)
    
    # Notes
    buyer_notes = Column(Text, nullable=True)
    nursery_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("seedling_listings.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class NurseryReview(Base):
    __tablename__ = "nursery_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    nursery_id = Column(Integer, ForeignKey("nurseries.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    
    rating = Column(Integer, nullable=False)  # 1-5 stars
    title = Column(String, nullable=True)
    comment = Column(Text, nullable=True)
    
    # Review categories
    seedling_quality = Column(Integer, nullable=True)  # 1-5
    delivery_speed = Column(Integer, nullable=True)  # 1-5
    customer_service = Column(Integer, nullable=True)  # 1-5
    
    is_verified_purchase = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
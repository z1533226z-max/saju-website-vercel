"""
Database Models for Saju Application
Using SQLAlchemy ORM
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum as PyEnum

from sqlalchemy import (
    create_engine, Column, String, Integer, BigInteger, Boolean, 
    DateTime, Date, Time, Text, JSON, DECIMAL, Enum, ForeignKey,
    Index, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from sqlalchemy.sql import func

Base = declarative_base()

# Enums
class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class AccountStatus(PyEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

class OAuthProvider(PyEnum):
    GOOGLE = "google"
    KAKAO = "kakao"
    NAVER = "naver"
    FACEBOOK = "facebook"

class CalculationType(PyEnum):
    BASIC = "basic"
    DETAILED = "detailed"
    COMPATIBILITY = "compatibility"
    YEARLY = "yearly"
    MAJOR = "major"

class FavoriteType(PyEnum):
    PROFILE = "profile"
    CALCULATION = "calculation"
    INTERPRETATION = "interpretation"

class ShareType(PyEnum):
    PUBLIC = "public"
    PASSWORD = "password"
    LINK_ONLY = "link_only"

class RelationshipType(PyEnum):
    ROMANTIC = "romantic"
    BUSINESS = "business"
    FRIENDSHIP = "friendship"
    FAMILY = "family"
    GENERAL = "general"


class User(Base):
    """User account model"""
    __tablename__ = 'users'
    
    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    full_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_time = Column(Time, nullable=True)
    birth_location = Column(String(255), nullable=True)
    is_lunar = Column(Boolean, default=False)
    gender = Column(Enum(Gender), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    
    # Authentication & Security
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    password_reset_expires = Column(DateTime, nullable=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # OAuth Integration
    oauth_provider = Column(Enum(OAuthProvider), nullable=True)
    oauth_provider_id = Column(String(255), nullable=True)
    
    # User Settings
    language_preference = Column(String(10), default='ko')
    timezone = Column(String(50), default='Asia/Seoul')
    notification_enabled = Column(Boolean, default=True)
    newsletter_subscribed = Column(Boolean, default=False)
    
    # Account Status
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    last_login_at = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    saju_profiles = relationship("SajuProfile", back_populates="user", cascade="all, delete-orphan")
    calculation_history = relationship("CalculationHistory", back_populates="user")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    collections = relationship("FavoriteCollection", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email='{self.email}')>"


class UserProfile(Base):
    """Extended user profile information"""
    __tablename__ = 'user_profiles'
    
    profile_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    # Additional Birth Information
    birth_city = Column(String(100), nullable=True)
    birth_country = Column(String(100), nullable=True)
    birth_latitude = Column(DECIMAL(10, 8), nullable=True)
    birth_longitude = Column(DECIMAL(11, 8), nullable=True)
    
    # Personal Preferences
    marital_status = Column(String(50), nullable=True)
    occupation = Column(String(100), nullable=True)
    interests = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Saju Preferences
    preferred_interpretation_style = Column(String(20), default='mixed')
    show_advanced_analysis = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user_profile'),
    )


class SajuProfile(Base):
    """Saju profile for storing multiple profiles per user"""
    __tablename__ = 'saju_profiles'
    
    profile_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    profile_name = Column(String(100), nullable=False)
    
    # Birth Information
    birth_year = Column(Integer, nullable=False)
    birth_month = Column(Integer, nullable=False)
    birth_day = Column(Integer, nullable=False)
    birth_hour = Column(Integer, nullable=False)
    birth_minute = Column(Integer, default=0)
    is_lunar = Column(Boolean, default=False)
    is_leap_month = Column(Boolean, default=False)
    
    # Personal Information
    gender = Column(Enum(Gender), nullable=False)
    full_name = Column(String(100), nullable=True)
    relationship_to_user = Column(String(100), nullable=True)
    
    # Calculated Saju Data (Cached)
    year_stem = Column(String(10), nullable=True)
    year_branch = Column(String(10), nullable=True)
    month_stem = Column(String(10), nullable=True)
    month_branch = Column(String(10), nullable=True)
    day_stem = Column(String(10), nullable=True)
    day_branch = Column(String(10), nullable=True)
    hour_stem = Column(String(10), nullable=True)
    hour_branch = Column(String(10), nullable=True)
    
    # Element Distribution
    wood_count = Column(Integer, default=0)
    fire_count = Column(Integer, default=0)
    earth_count = Column(Integer, default=0)
    metal_count = Column(Integer, default=0)
    water_count = Column(Integer, default=0)
    
    # Ten Gods Distribution
    ten_gods_json = Column(JSON, nullable=True)
    
    # Profile Settings
    is_public = Column(Boolean, default=False)
    is_primary = Column(Boolean, default=False)
    color_theme = Column(String(7), nullable=True)
    icon_emoji = Column(String(10), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_calculated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="saju_profiles")
    calculation_history = relationship("CalculationHistory", back_populates="profile")
    favorites = relationship("Favorite", back_populates="profile")
    
    def __repr__(self):
        return f"<SajuProfile(profile_id={self.profile_id}, name='{self.profile_name}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            'profile_id': self.profile_id,
            'profile_name': self.profile_name,
            'birth_date': f"{self.birth_year}-{self.birth_month:02d}-{self.birth_day:02d}",
            'birth_time': f"{self.birth_hour:02d}:{self.birth_minute:02d}",
            'is_lunar': self.is_lunar,
            'gender': self.gender.value if self.gender else None,
            'four_pillars': {
                'year': {'stem': self.year_stem, 'branch': self.year_branch},
                'month': {'stem': self.month_stem, 'branch': self.month_branch},
                'day': {'stem': self.day_stem, 'branch': self.day_branch},
                'hour': {'stem': self.hour_stem, 'branch': self.hour_branch}
            },
            'elements': {
                'wood': self.wood_count,
                'fire': self.fire_count,
                'earth': self.earth_count,
                'metal': self.metal_count,
                'water': self.water_count
            },
            'ten_gods': self.ten_gods_json
        }


class CalculationHistory(Base):
    """History of all Saju calculations"""
    __tablename__ = 'calculation_history'
    
    history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    profile_id = Column(BigInteger, ForeignKey('saju_profiles.profile_id', ondelete='SET NULL'), nullable=True)
    session_id = Column(String(100), nullable=True)
    
    # Input Data
    input_data = Column(JSON, nullable=False)
    birth_date = Column(Date, nullable=False)
    birth_time = Column(Time, nullable=False)
    is_lunar = Column(Boolean, default=False)
    gender = Column(String(10), nullable=True)
    
    # Calculation Results
    result_data = Column(JSON, nullable=False)
    four_pillars = Column(JSON, nullable=True)
    elements_distribution = Column(JSON, nullable=True)
    ten_gods = Column(JSON, nullable=True)
    
    # Interpretation Data
    interpretation_basic = Column(Text, nullable=True)
    interpretation_personality = Column(Text, nullable=True)
    interpretation_career = Column(Text, nullable=True)
    interpretation_wealth = Column(Text, nullable=True)
    interpretation_relationship = Column(Text, nullable=True)
    interpretation_health = Column(Text, nullable=True)
    
    # Fortune Data
    major_fortune_data = Column(JSON, nullable=True)
    current_major_fortune = Column(JSON, nullable=True)
    yearly_fortune_data = Column(JSON, nullable=True)
    current_year_fortune = Column(JSON, nullable=True)
    
    # Calculation Metadata
    calculation_type = Column(Enum(CalculationType), default=CalculationType.BASIC)
    calculation_duration_ms = Column(Integer, nullable=True)
    api_version = Column(String(20), nullable=True)
    client_ip = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Analytics
    view_count = Column(Integer, default=1)
    share_count = Column(Integer, default=0)
    export_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="calculation_history")
    profile = relationship("SajuProfile", back_populates="calculation_history")
    favorites = relationship("Favorite", back_populates="history")
    shared_results = relationship("SharedResult", back_populates="history", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CalculationHistory(history_id={self.history_id}, date={self.birth_date})>"


class Favorite(Base):
    """User favorites for profiles and calculations"""
    __tablename__ = 'favorites'
    
    favorite_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    profile_id = Column(BigInteger, ForeignKey('saju_profiles.profile_id', ondelete='CASCADE'), nullable=True)
    history_id = Column(BigInteger, ForeignKey('calculation_history.history_id', ondelete='CASCADE'), nullable=True)
    
    # Favorite Details
    favorite_type = Column(Enum(FavoriteType), nullable=False)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)
    
    # Custom Categories
    category = Column(String(50), nullable=True)
    color_label = Column(String(7), nullable=True)
    
    # Display Settings
    is_pinned = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    
    # Sharing
    is_shared = Column(Boolean, default=False)
    share_token = Column(String(100), unique=True, nullable=True)
    share_expires_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_accessed_at = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    profile = relationship("SajuProfile", back_populates="favorites")
    history = relationship("CalculationHistory", back_populates="favorites")
    collection_items = relationship("CollectionItem", back_populates="favorite", cascade="all, delete-orphan")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'profile_id', 'history_id', name='unique_user_favorite'),
        Index('idx_user_favorites', 'user_id', 'is_pinned', 'sort_order'),
        Index('idx_category', 'user_id', 'category'),
    )


class FavoriteCollection(Base):
    """Collections for organizing favorites"""
    __tablename__ = 'favorite_collections'
    
    collection_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    collection_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon_emoji = Column(String(10), nullable=True)
    color_theme = Column(String(7), nullable=True)
    
    # Privacy Settings
    is_public = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    share_token = Column(String(100), unique=True, nullable=True)
    
    # Statistics
    item_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="collections")
    items = relationship("CollectionItem", back_populates="collection", cascade="all, delete-orphan")


class CollectionItem(Base):
    """Items in a favorite collection"""
    __tablename__ = 'collection_items'
    
    item_id = Column(BigInteger, primary_key=True, autoincrement=True)
    collection_id = Column(BigInteger, ForeignKey('favorite_collections.collection_id', ondelete='CASCADE'), nullable=False)
    favorite_id = Column(BigInteger, ForeignKey('favorites.favorite_id', ondelete='CASCADE'), nullable=False)
    
    sort_order = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    
    added_at = Column(DateTime, default=func.now())
    
    # Relationships
    collection = relationship("FavoriteCollection", back_populates="items")
    favorite = relationship("Favorite", back_populates="collection_items")
    
    __table_args__ = (
        UniqueConstraint('collection_id', 'favorite_id', name='unique_collection_item'),
        Index('idx_collection_items', 'collection_id', 'sort_order'),
    )


class SharedResult(Base):
    """Shared Saju calculation results"""
    __tablename__ = 'shared_results'
    
    share_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    history_id = Column(BigInteger, ForeignKey('calculation_history.history_id', ondelete='CASCADE'), nullable=True)
    profile_id = Column(BigInteger, ForeignKey('saju_profiles.profile_id', ondelete='CASCADE'), nullable=True)
    
    # Share Details
    share_token = Column(String(100), unique=True, nullable=False)
    short_url = Column(String(50), unique=True, nullable=True)
    qr_code_url = Column(String(500), nullable=True)
    
    # Share Settings
    share_type = Column(Enum(ShareType), default=ShareType.LINK_ONLY)
    password_hash = Column(String(255), nullable=True)
    
    # Access Control
    max_views = Column(Integer, nullable=True)
    current_views = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Analytics
    view_analytics = Column(JSON, nullable=True)
    last_viewed_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    history = relationship("CalculationHistory", back_populates="shared_results")


class CompatibilityCalculation(Base):
    """Compatibility calculations between profiles"""
    __tablename__ = 'compatibility_calculations'
    
    compatibility_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    
    # Profiles Being Compared
    profile1_id = Column(BigInteger, ForeignKey('saju_profiles.profile_id', ondelete='CASCADE'), nullable=False)
    profile2_id = Column(BigInteger, ForeignKey('saju_profiles.profile_id', ondelete='CASCADE'), nullable=False)
    
    # Compatibility Results
    overall_score = Column(Integer, nullable=True)
    element_harmony_score = Column(Integer, nullable=True)
    pillar_compatibility_score = Column(Integer, nullable=True)
    ten_gods_balance_score = Column(Integer, nullable=True)
    
    # Detailed Analysis
    compatibility_data = Column(JSON, nullable=True)
    strengths = Column(Text, nullable=True)
    challenges = Column(Text, nullable=True)
    advice = Column(Text, nullable=True)
    
    # Relationship Type
    relationship_type = Column(Enum(RelationshipType), default=RelationshipType.GENERAL)
    
    created_at = Column(DateTime, default=func.now())


class UserSession(Base):
    """User session management"""
    __tablename__ = 'user_sessions'
    
    session_id = Column(String(100), primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=True)
    
    # Session Data
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_type = Column(String(50), nullable=True)
    browser = Column(String(50), nullable=True)
    os = Column(String(50), nullable=True)
    
    # Session State
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime, nullable=True)
    
    # Session Data Storage
    session_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    __table_args__ = (
        Index('idx_user_sessions', 'user_id', 'is_active'),
        Index('idx_expires', 'expires_at'),
    )


# Database connection setup
def get_database_url(config: Dict[str, str]) -> str:
    """Generate database URL from configuration"""
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset=utf8mb4"


def init_database(database_url: str):
    """Initialize database connection and create tables"""
    engine = create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create session factory
    Session = sessionmaker(bind=engine)
    
    return engine, Session
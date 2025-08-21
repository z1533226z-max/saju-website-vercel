"""
Database Service Layer for Saju Application
Implements repository pattern for database operations
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import hashlib
import secrets
import json

from models.database import (
    User, UserProfile, SajuProfile, CalculationHistory,
    Favorite, FavoriteCollection, CollectionItem,
    SharedResult, CompatibilityCalculation, UserSession,
    FavoriteType, CalculationType, ShareType
)


class UserRepository:
    """Repository for user-related database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, **kwargs) -> User:
        """Create a new user"""
        user = User(email=email, **kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.user_id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_last_login(self, user_id: int) -> None:
        """Update user's last login time"""
        user = self.get_user_by_id(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            user.login_count += 1
            self.db.commit()


class SajuProfileRepository:
    """Repository for Saju profile operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_profile(self, user_id: int, profile_data: Dict[str, Any]) -> SajuProfile:
        """Create a new Saju profile"""
        profile = SajuProfile(user_id=user_id, **profile_data)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
    
    def get_profile_by_id(self, profile_id: int) -> Optional[SajuProfile]:
        """Get profile by ID"""
        return self.db.query(SajuProfile).filter(
            SajuProfile.profile_id == profile_id
        ).first()
    
    def get_user_profiles(self, user_id: int) -> List[SajuProfile]:
        """Get all profiles for a user"""
        return self.db.query(SajuProfile).filter(
            SajuProfile.user_id == user_id
        ).order_by(
            desc(SajuProfile.is_primary),
            desc(SajuProfile.created_at)
        ).all()
    
    def get_primary_profile(self, user_id: int) -> Optional[SajuProfile]:
        """Get user's primary profile"""
        return self.db.query(SajuProfile).filter(
            and_(
                SajuProfile.user_id == user_id,
                SajuProfile.is_primary == True
            )
        ).first()
    
    def update_profile(self, profile_id: int, **kwargs) -> Optional[SajuProfile]:
        """Update profile information"""
        profile = self.get_profile_by_id(profile_id)
        if profile:
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            profile.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(profile)
        return profile
    
    def update_calculated_data(self, profile_id: int, saju_data: Dict[str, Any]) -> None:
        """Update profile with calculated Saju data"""
        profile = self.get_profile_by_id(profile_id)
        if profile:
            # Update four pillars
            if 'year' in saju_data:
                profile.year_stem = saju_data['year'].get('heavenly')
                profile.year_branch = saju_data['year'].get('earthly')
            if 'month' in saju_data:
                profile.month_stem = saju_data['month'].get('heavenly')
                profile.month_branch = saju_data['month'].get('earthly')
            if 'day' in saju_data:
                profile.day_stem = saju_data['day'].get('heavenly')
                profile.day_branch = saju_data['day'].get('earthly')
            if 'hour' in saju_data:
                profile.hour_stem = saju_data['hour'].get('heavenly')
                profile.hour_branch = saju_data['hour'].get('earthly')
            
            # Update elements
            if 'elements' in saju_data:
                elements = saju_data['elements'].get('distribution', {})
                profile.wood_count = elements.get('목', 0)
                profile.fire_count = elements.get('화', 0)
                profile.earth_count = elements.get('토', 0)
                profile.metal_count = elements.get('금', 0)
                profile.water_count = elements.get('수', 0)
            
            # Update ten gods
            if 'ten_gods' in saju_data:
                profile.ten_gods_json = saju_data['ten_gods']
            
            profile.last_calculated_at = datetime.utcnow()
            self.db.commit()
    
    def delete_profile(self, profile_id: int) -> bool:
        """Delete a profile"""
        profile = self.get_profile_by_id(profile_id)
        if profile:
            self.db.delete(profile)
            self.db.commit()
            return True
        return False


class CalculationHistoryRepository:
    """Repository for calculation history operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_calculation(self, calculation_data: Dict[str, Any]) -> CalculationHistory:
        """Save a calculation to history"""
        history = CalculationHistory(**calculation_data)
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history
    
    def get_history_by_id(self, history_id: int) -> Optional[CalculationHistory]:
        """Get calculation history by ID"""
        return self.db.query(CalculationHistory).filter(
            CalculationHistory.history_id == history_id
        ).first()
    
    def get_user_history(
        self, 
        user_id: int, 
        limit: int = 50,
        offset: int = 0,
        calculation_type: Optional[CalculationType] = None
    ) -> List[CalculationHistory]:
        """Get user's calculation history"""
        query = self.db.query(CalculationHistory).filter(
            CalculationHistory.user_id == user_id
        )
        
        if calculation_type:
            query = query.filter(CalculationHistory.calculation_type == calculation_type)
        
        return query.order_by(
            desc(CalculationHistory.created_at)
        ).limit(limit).offset(offset).all()
    
    def get_recent_calculations(
        self, 
        user_id: int, 
        days: int = 30
    ) -> List[CalculationHistory]:
        """Get recent calculations within specified days"""
        since_date = datetime.utcnow() - timedelta(days=days)
        
        return self.db.query(CalculationHistory).filter(
            and_(
                CalculationHistory.user_id == user_id,
                CalculationHistory.created_at >= since_date
            )
        ).order_by(desc(CalculationHistory.created_at)).all()
    
    def increment_view_count(self, history_id: int) -> None:
        """Increment view count for a calculation"""
        history = self.get_history_by_id(history_id)
        if history:
            history.view_count += 1
            self.db.commit()
    
    def get_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get user's calculation statistics"""
        total_calculations = self.db.query(func.count(CalculationHistory.history_id)).filter(
            CalculationHistory.user_id == user_id
        ).scalar()
        
        calculations_by_type = self.db.query(
            CalculationHistory.calculation_type,
            func.count(CalculationHistory.history_id)
        ).filter(
            CalculationHistory.user_id == user_id
        ).group_by(CalculationHistory.calculation_type).all()
        
        return {
            'total_calculations': total_calculations,
            'by_type': {str(calc_type): count for calc_type, count in calculations_by_type},
            'recent_count': len(self.get_recent_calculations(user_id, days=7))
        }


class FavoriteRepository:
    """Repository for favorites operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def add_favorite(
        self, 
        user_id: int,
        favorite_type: FavoriteType,
        profile_id: Optional[int] = None,
        history_id: Optional[int] = None,
        **kwargs
    ) -> Favorite:
        """Add a new favorite"""
        # Check if already favorited
        existing = self.db.query(Favorite).filter(
            and_(
                Favorite.user_id == user_id,
                Favorite.profile_id == profile_id,
                Favorite.history_id == history_id
            )
        ).first()
        
        if existing:
            return existing
        
        favorite = Favorite(
            user_id=user_id,
            favorite_type=favorite_type,
            profile_id=profile_id,
            history_id=history_id,
            **kwargs
        )
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite
    
    def get_favorite_by_id(self, favorite_id: int) -> Optional[Favorite]:
        """Get favorite by ID"""
        return self.db.query(Favorite).filter(
            Favorite.favorite_id == favorite_id
        ).first()
    
    def get_user_favorites(
        self, 
        user_id: int,
        favorite_type: Optional[FavoriteType] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Favorite]:
        """Get user's favorites"""
        query = self.db.query(Favorite).filter(Favorite.user_id == user_id)
        
        if favorite_type:
            query = query.filter(Favorite.favorite_type == favorite_type)
        
        if category:
            query = query.filter(Favorite.category == category)
        
        return query.order_by(
            desc(Favorite.is_pinned),
            Favorite.sort_order,
            desc(Favorite.created_at)
        ).limit(limit).offset(offset).all()
    
    def get_pinned_favorites(self, user_id: int) -> List[Favorite]:
        """Get user's pinned favorites"""
        return self.db.query(Favorite).filter(
            and_(
                Favorite.user_id == user_id,
                Favorite.is_pinned == True
            )
        ).order_by(Favorite.sort_order).all()
    
    def update_favorite(self, favorite_id: int, **kwargs) -> Optional[Favorite]:
        """Update favorite"""
        favorite = self.get_favorite_by_id(favorite_id)
        if favorite:
            for key, value in kwargs.items():
                if hasattr(favorite, key):
                    setattr(favorite, key, value)
            favorite.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(favorite)
        return favorite
    
    def toggle_pin(self, favorite_id: int) -> bool:
        """Toggle pin status of a favorite"""
        favorite = self.get_favorite_by_id(favorite_id)
        if favorite:
            favorite.is_pinned = not favorite.is_pinned
            self.db.commit()
            return True
        return False
    
    def update_access(self, favorite_id: int) -> None:
        """Update last accessed time and count"""
        favorite = self.get_favorite_by_id(favorite_id)
        if favorite:
            favorite.last_accessed_at = datetime.utcnow()
            favorite.access_count += 1
            self.db.commit()
    
    def delete_favorite(self, favorite_id: int) -> bool:
        """Delete a favorite"""
        favorite = self.get_favorite_by_id(favorite_id)
        if favorite:
            self.db.delete(favorite)
            self.db.commit()
            return True
        return False


class FavoriteCollectionRepository:
    """Repository for favorite collections"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_collection(self, user_id: int, name: str, **kwargs) -> FavoriteCollection:
        """Create a new collection"""
        collection = FavoriteCollection(
            user_id=user_id,
            collection_name=name,
            **kwargs
        )
        self.db.add(collection)
        self.db.commit()
        self.db.refresh(collection)
        return collection
    
    def get_collection_by_id(self, collection_id: int) -> Optional[FavoriteCollection]:
        """Get collection by ID"""
        return self.db.query(FavoriteCollection).filter(
            FavoriteCollection.collection_id == collection_id
        ).first()
    
    def get_user_collections(self, user_id: int) -> List[FavoriteCollection]:
        """Get all collections for a user"""
        return self.db.query(FavoriteCollection).filter(
            FavoriteCollection.user_id == user_id
        ).order_by(FavoriteCollection.created_at).all()
    
    def add_to_collection(
        self, 
        collection_id: int, 
        favorite_id: int,
        notes: Optional[str] = None
    ) -> Optional[CollectionItem]:
        """Add a favorite to a collection"""
        # Check if already in collection
        existing = self.db.query(CollectionItem).filter(
            and_(
                CollectionItem.collection_id == collection_id,
                CollectionItem.favorite_id == favorite_id
            )
        ).first()
        
        if existing:
            return existing
        
        item = CollectionItem(
            collection_id=collection_id,
            favorite_id=favorite_id,
            notes=notes
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def remove_from_collection(self, collection_id: int, favorite_id: int) -> bool:
        """Remove a favorite from a collection"""
        item = self.db.query(CollectionItem).filter(
            and_(
                CollectionItem.collection_id == collection_id,
                CollectionItem.favorite_id == favorite_id
            )
        ).first()
        
        if item:
            self.db.delete(item)
            self.db.commit()
            return True
        return False
    
    def get_collection_items(self, collection_id: int) -> List[CollectionItem]:
        """Get all items in a collection"""
        return self.db.query(CollectionItem).filter(
            CollectionItem.collection_id == collection_id
        ).order_by(CollectionItem.sort_order).all()


class SharedResultRepository:
    """Repository for shared results"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_share(
        self,
        user_id: Optional[int],
        history_id: Optional[int],
        profile_id: Optional[int],
        share_type: ShareType = ShareType.LINK_ONLY,
        expires_days: int = 30,
        **kwargs
    ) -> SharedResult:
        """Create a shared result"""
        share_token = self._generate_share_token()
        short_url = self._generate_short_url()
        expires_at = datetime.utcnow() + timedelta(days=expires_days) if expires_days else None
        
        shared = SharedResult(
            user_id=user_id,
            history_id=history_id,
            profile_id=profile_id,
            share_token=share_token,
            short_url=short_url,
            share_type=share_type,
            expires_at=expires_at,
            **kwargs
        )
        self.db.add(shared)
        self.db.commit()
        self.db.refresh(shared)
        return shared
    
    def get_by_token(self, share_token: str) -> Optional[SharedResult]:
        """Get shared result by token"""
        return self.db.query(SharedResult).filter(
            and_(
                SharedResult.share_token == share_token,
                SharedResult.is_active == True
            )
        ).first()
    
    def get_by_short_url(self, short_url: str) -> Optional[SharedResult]:
        """Get shared result by short URL"""
        return self.db.query(SharedResult).filter(
            and_(
                SharedResult.short_url == short_url,
                SharedResult.is_active == True
            )
        ).first()
    
    def increment_view(self, share_id: int) -> None:
        """Increment view count for shared result"""
        shared = self.db.query(SharedResult).filter(
            SharedResult.share_id == share_id
        ).first()
        
        if shared:
            shared.current_views += 1
            shared.last_viewed_at = datetime.utcnow()
            
            # Update analytics
            if not shared.view_analytics:
                shared.view_analytics = {}
            
            today = datetime.utcnow().date().isoformat()
            if 'daily_views' not in shared.view_analytics:
                shared.view_analytics['daily_views'] = {}
            
            shared.view_analytics['daily_views'][today] = \
                shared.view_analytics['daily_views'].get(today, 0) + 1
            
            # Check if max views reached
            if shared.max_views and shared.current_views >= shared.max_views:
                shared.is_active = False
            
            self.db.commit()
    
    def check_expired(self) -> int:
        """Deactivate expired shares and return count"""
        expired = self.db.query(SharedResult).filter(
            and_(
                SharedResult.expires_at < datetime.utcnow(),
                SharedResult.is_active == True
            )
        ).all()
        
        count = len(expired)
        for share in expired:
            share.is_active = False
        
        self.db.commit()
        return count
    
    def _generate_share_token(self) -> str:
        """Generate unique share token"""
        return secrets.token_urlsafe(32)
    
    def _generate_short_url(self) -> str:
        """Generate short URL identifier"""
        return secrets.token_urlsafe(6)


class CompatibilityRepository:
    """Repository for compatibility calculations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_compatibility(
        self,
        user_id: Optional[int],
        profile1_id: int,
        profile2_id: int,
        compatibility_data: Dict[str, Any]
    ) -> CompatibilityCalculation:
        """Save compatibility calculation"""
        compatibility = CompatibilityCalculation(
            user_id=user_id,
            profile1_id=profile1_id,
            profile2_id=profile2_id,
            **compatibility_data
        )
        self.db.add(compatibility)
        self.db.commit()
        self.db.refresh(compatibility)
        return compatibility
    
    def get_compatibility_history(
        self,
        user_id: int,
        limit: int = 20
    ) -> List[CompatibilityCalculation]:
        """Get user's compatibility calculation history"""
        return self.db.query(CompatibilityCalculation).filter(
            CompatibilityCalculation.user_id == user_id
        ).order_by(
            desc(CompatibilityCalculation.created_at)
        ).limit(limit).all()


# Database service facade
class DatabaseService:
    """Main database service that aggregates all repositories"""
    
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.profiles = SajuProfileRepository(db)
        self.history = CalculationHistoryRepository(db)
        self.favorites = FavoriteRepository(db)
        self.collections = FavoriteCollectionRepository(db)
        self.shares = SharedResultRepository(db)
        self.compatibility = CompatibilityRepository(db)
    
    def commit(self):
        """Commit current transaction"""
        self.db.commit()
    
    def rollback(self):
        """Rollback current transaction"""
        self.db.rollback()
    
    def close(self):
        """Close database session"""
        self.db.close()
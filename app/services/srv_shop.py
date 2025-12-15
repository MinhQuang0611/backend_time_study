from typing import Optional
from fastapi_sqlalchemy import db
from app.models.model_shop import ShopEntity, ShopPurchaseEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from app.utils import time_utils


class ShopService(BaseService[ShopEntity]):

    def __init__(self):
        super().__init__(ShopEntity)


class ShopPurchaseService(BaseService[ShopPurchaseEntity]):

    def __init__(self):
        super().__init__(ShopPurchaseEntity)
    
    def purchase_item(self, user_id: int, shop_id: int) -> ShopPurchaseEntity:
        """Purchase a shop item for a user"""
        # Check if already purchased
        existing_purchase = db.session.query(ShopPurchaseEntity).filter(
            ShopPurchaseEntity.user_id == user_id,
            ShopPurchaseEntity.shop_id == shop_id
        ).first()
        
        if existing_purchase:
            raise CustomException(
                exception=ExceptionType.BAD_REQUEST,
                message="Sản phẩm này đã được mua rồi"
            )
        
        # Create new purchase
        purchase_data = {
            "user_id": user_id,
            "shop_id": shop_id,
            "purchased_at": time_utils.timestamp_now()
        }
        return self.create(data=purchase_data)
    
    def get_purchase_status(self, user_id: int, shop_id: int) -> Optional[ShopPurchaseEntity]:
        """Get purchase status for a user and shop item"""
        return db.session.query(ShopPurchaseEntity).filter(
            ShopPurchaseEntity.user_id == user_id,
            ShopPurchaseEntity.shop_id == shop_id
        ).first()


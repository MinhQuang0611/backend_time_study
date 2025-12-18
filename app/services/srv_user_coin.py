from fastapi_sqlalchemy import db
from app.models.model_user_coin import UserCoinEntity
from app.services.srv_base import BaseService
from app.utils.exception_handler import CustomException, ExceptionType
from typing import Any, Dict, Optional


class UserCoinService(BaseService[UserCoinEntity]):

    def __init__(self):
        super().__init__(UserCoinEntity)

    def get_or_create_coin(self, user_id: int) -> UserCoinEntity:
        """
        Lấy coin của user, nếu chưa có thì tạo mới với coin = 0
        """
        coin = db.session.query(UserCoinEntity).filter(
            UserCoinEntity.user_id == user_id
        ).first()
        
        if not coin:
            coin = self.create(data={"user_id": user_id, "coin": 0})
        
        return coin

    def get_coin(self, user_id: int) -> int:
        """
        Lấy số coin hiện tại của user
        """
        coin = self.get_or_create_coin(user_id)
        return coin.coin

    def add_coin(self, user_id: int, amount: int) -> UserCoinEntity:
        """
        Thêm coin cho user
        """
        coin = self.get_or_create_coin(user_id)
        coin.coin += amount
        if coin.coin < 0:
            coin.coin = 0
        db.session.commit()
        db.session.refresh(coin)
        return coin

    def subtract_coin(self, user_id: int, amount: int) -> UserCoinEntity:
        """
        Trừ coin của user (kiểm tra đủ coin trước khi trừ)
        """
        coin = self.get_or_create_coin(user_id)
        
        if coin.coin < amount:
            raise CustomException(
                exception=ExceptionType.BAD_REQUEST,
                message=f"Không đủ coin. Hiện tại có {coin.coin} coin, cần {amount} coin"
            )
        
        coin.coin -= amount
        db.session.commit()
        db.session.refresh(coin)
        return coin

    def set_coin(self, user_id: int, coin_amount: int) -> UserCoinEntity:
        """
        Set số coin cho user
        """
        coin = self.get_or_create_coin(user_id)
        coin.coin = max(0, coin_amount)  # Đảm bảo không âm
        db.session.commit()
        db.session.refresh(coin)
        return coin


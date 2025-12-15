from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_shop import (
    ShopCreateRequest,
    ShopUpdateRequest,
    ShopBaseResponse,
    ShopWithPurchaseStatusResponse,
    ShopPurchaseRequest,
    ShopPurchaseResponse,
)
from app.services.srv_shop import ShopService, ShopPurchaseService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/shop")

shop_service: ShopService = ShopService()
shop_purchase_service: ShopPurchaseService = ShopPurchaseService()


@router.post(
    "",
    response_model=DataResponse[ShopBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_shop_item(
    shop_data: ShopCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Tạo sản phẩm mới trong shop (Admin hoặc bất kỳ user nào)
    """
    try:
        new_shop = shop_service.create(data=shop_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_shop)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "",
    response_model=DataResponse[List[ShopWithPurchaseStatusResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_shop_items(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy tất cả sản phẩm với trạng thái mua của user hiện tại
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_shop import ShopEntity, ShopPurchaseEntity
        from app.utils.paging import paginate
        
        # Get all shop items
        query = db.session.query(ShopEntity)
        shops, metadata = paginate(
            model=ShopEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        
        # Get all purchase statuses for current user
        purchase_statuses = {
            p.shop_id: p
            for p in db.session.query(ShopPurchaseEntity).filter(
                ShopPurchaseEntity.user_id == current_user.user_id
            ).all()
        }
        
        # Combine shop items with purchase status
        result = []
        for shop in shops:
            purchase = purchase_statuses.get(shop.shop_id)
            result.append({
                "shop_id": shop.shop_id,
                "name": shop.name,
                "price": shop.price,
                "type": shop.type,
                "is_purchased": purchase is not None,
                "purchased_at": purchase.purchased_at if purchase else None,
                "created_at": shop.created_at,
                "updated_at": shop.updated_at,
            })
        
        return DataResponse(http_code=status.HTTP_200_OK, data=result, metadata=metadata)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/purchased",
    response_model=DataResponse[List[ShopWithPurchaseStatusResponse]],
    status_code=status.HTTP_200_OK,
)
def get_purchased_items(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy danh sách sản phẩm đã mua của user hiện tại
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_shop import ShopEntity, ShopPurchaseEntity
        from app.utils.paging import paginate
        
        # Get all purchases for current user
        purchases_query = db.session.query(ShopPurchaseEntity).filter(
            ShopPurchaseEntity.user_id == current_user.user_id
        )
        
        # Join with shop to get shop details
        query = db.session.query(ShopEntity).join(
            ShopPurchaseEntity,
            ShopEntity.shop_id == ShopPurchaseEntity.shop_id
        ).filter(
            ShopPurchaseEntity.user_id == current_user.user_id
        )
        
        shops, metadata = paginate(
            model=ShopEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        
        # Get purchase info
        purchase_map = {
            p.shop_id: p
            for p in purchases_query.all()
        }
        
        # Format response
        result = []
        for shop in shops:
            purchase = purchase_map.get(shop.shop_id)
            result.append({
                "shop_id": shop.shop_id,
                "name": shop.name,
                "price": shop.price,
                "type": shop.type,
                "is_purchased": True,
                "purchased_at": purchase.purchased_at if purchase else None,
                "created_at": shop.created_at,
                "updated_at": shop.updated_at,
            })
        
        return DataResponse(http_code=status.HTTP_200_OK, data=result, metadata=metadata)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/not-purchased",
    response_model=DataResponse[List[ShopWithPurchaseStatusResponse]],
    status_code=status.HTTP_200_OK,
)
def get_not_purchased_items(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy danh sách sản phẩm chưa mua của user hiện tại
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_shop import ShopEntity, ShopPurchaseEntity
        from sqlalchemy import not_
        from app.utils.paging import paginate
        
        # Get all shop IDs that user has purchased
        purchased_shop_ids = [
            shop_id for shop_id, in db.session.query(ShopPurchaseEntity.shop_id).filter(
                ShopPurchaseEntity.user_id == current_user.user_id
            ).all()
        ]
        
        # Get all shop items that user hasn't purchased
        if purchased_shop_ids:
            query = db.session.query(ShopEntity).filter(
                not_(ShopEntity.shop_id.in_(purchased_shop_ids))
            )
        else:
            # If user hasn't purchased anything, return all items
            query = db.session.query(ShopEntity)
        
        shops, metadata = paginate(
            model=ShopEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        
        # Format response
        result = []
        for shop in shops:
            result.append({
                "shop_id": shop.shop_id,
                "name": shop.name,
                "price": shop.price,
                "type": shop.type,
                "is_purchased": False,
                "purchased_at": None,
                "created_at": shop.created_at,
                "updated_at": shop.updated_at,
            })
        
        return DataResponse(http_code=status.HTTP_200_OK, data=result, metadata=metadata)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{shop_id}",
    response_model=DataResponse[ShopWithPurchaseStatusResponse],
    status_code=status.HTTP_200_OK,
)
def get_shop_item_by_id(
    shop_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Lấy thông tin sản phẩm và trạng thái mua của user hiện tại
    """
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_shop import ShopEntity, ShopPurchaseEntity
        
        shop = shop_service.get_by_id(shop_id)
        
        # Check purchase status
        purchase = shop_purchase_service.get_purchase_status(
            user_id=current_user.user_id,
            shop_id=shop_id
        )
        
        result = {
            "shop_id": shop.shop_id,
            "name": shop.name,
            "price": shop.price,
            "type": shop.type,
            "is_purchased": purchase is not None,
            "purchased_at": purchase.purchased_at if purchase else None,
            "created_at": shop.created_at,
            "updated_at": shop.updated_at,
        }
        
        return DataResponse(http_code=status.HTTP_200_OK, data=result)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{shop_id}/status",
    response_model=DataResponse[dict],
    status_code=status.HTTP_200_OK,
)
def get_purchase_status(
    shop_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Kiểm tra trạng thái đã mua hay chưa của sản phẩm
    """
    try:
        # Verify shop exists
        shop_service.get_by_id(shop_id)
        
        # Check purchase status
        purchase = shop_purchase_service.get_purchase_status(
            user_id=current_user.user_id,
            shop_id=shop_id
        )
        
        result = {
            "shop_id": shop_id,
            "is_purchased": purchase is not None,
            "purchased_at": purchase.purchased_at if purchase else None,
        }
        
        return DataResponse(http_code=status.HTTP_200_OK, data=result)
    except Exception as e:
        raise CustomException(exception=e)


@router.post(
    "/{shop_id}/purchase",
    response_model=DataResponse[ShopPurchaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def purchase_shop_item(
    shop_id: int,
    purchase_data: ShopPurchaseRequest = None,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Mua sản phẩm (user mua sản phẩm)
    """
    try:
        # Verify shop exists
        shop_service.get_by_id(shop_id)
        
        # Purchase item
        purchase = shop_purchase_service.purchase_item(
            user_id=current_user.user_id,
            shop_id=shop_id
        )
        
        result = {
            "purchase_id": purchase.purchase_id,
            "user_id": purchase.user_id,
            "shop_id": purchase.shop_id,
            "purchased_at": purchase.purchased_at,
            "created_at": purchase.created_at,
            "updated_at": purchase.updated_at,
        }
        
        return DataResponse(http_code=status.HTTP_201_CREATED, data=result)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{shop_id}",
    response_model=DataResponse[ShopBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_shop_item(
    shop_id: int,
    shop_data: ShopUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Cập nhật thông tin sản phẩm (Admin)
    """
    try:
        updated_shop = shop_service.update_by_id(shop_id, data=shop_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_shop)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{shop_id}",
    response_model=DataResponse[dict],
    status_code=status.HTTP_200_OK,
)
def delete_shop_item(
    shop_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    """
    Xóa sản phẩm (Admin)
    """
    try:
        shop_service.delete_by_id(shop_id)
        return DataResponse(http_code=status.HTTP_200_OK, data={"message": "Shop item deleted successfully"})
    except Exception as e:
        raise CustomException(exception=e)

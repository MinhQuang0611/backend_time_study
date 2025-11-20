from typing import Optional, List, Any
from sqlalchemy import asc, desc
from sqlalchemy.orm import Query
from app.schemas.sche_response import MetadataResponse
from app.utils.exception_handler import CustomException
from app.schemas.sche_base import PaginationParams, SortParams


def paginate(
    model,
    query: Query,
    pagination_params: Optional[PaginationParams] = None,
    sort_params: Optional[SortParams] = None,
):
    try:
        total = query.count()

        # Default metadata
        page = 1
        page_size = total

        # Sorting
        if sort_params and sort_params.sort_by:
            # fallback nếu thuộc tính không tồn tại
            if hasattr(model, sort_params.sort_by):
                direction_func = desc if sort_params.order == "desc" else asc
                query = query.order_by(direction_func(getattr(model, sort_params.sort_by)))
            else:
                # fallback về khóa chính (nếu model có user_id, id, etc.)
                primary_keys = [key.name for key in model.__table__.primary_key]
                if primary_keys:
                    direction_func = desc if sort_params.order == "desc" else asc
                    query = query.order_by(direction_func(getattr(model, primary_keys[0])))
        
        # Pagination
        if pagination_params:
            if pagination_params.page_size:
                page_size = pagination_params.page_size
                query = query.limit(page_size)
            if pagination_params.page:
                page = pagination_params.page
                query = query.offset(page_size * (page - 1))

        metadata = MetadataResponse(
            page=page,
            page_size=page_size,
            total=total,
        )

        data = query.all()
        print("============ PAGINATE ============", data, metadata, flush=True)

    except Exception as e:
        raise CustomException(exception=e)

    return data, metadata
from typing import Generic, TypeVar, Type, Any, Optional, List, Tuple, Dict

from fastapi.encoders import jsonable_encoder
from fastapi_sqlalchemy import db
from sqlalchemy.inspection import inspect

from app.models.model_base import Base
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_base import PaginationParams, SortParams
from app.utils.paging import paginate
from app.schemas.sche_response import MetadataResponse


ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType], object):

    def __init__(self, model: Type[ModelType]):
        self.model = model
        mapper = inspect(self.model)
        self.pk_field = mapper.primary_key[0].name if mapper.primary_key else "id"

    def _commit(self) -> None:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def _get_by_pk(self, value: Any) -> Optional[ModelType]:
        pk_column = getattr(self.model, self.pk_field)
        return db.session.query(self.model).filter(pk_column == value).first()

    def get_by_id(self, pk_value: Any) -> ModelType:
        obj = self._get_by_pk(pk_value)
        if obj is None:
            raise CustomException(exception=ExceptionType.NOT_FOUND)
        return obj

    def get_by_id_optional(self, pk_value: Any) -> Optional[ModelType]:
        return self._get_by_pk(pk_value)

    def get_all(
        self, sort_params: Optional[SortParams] = SortParams()
    ) -> Tuple[List[ModelType], MetadataResponse]:
        query = db.session.query(self.model)
        return paginate(
            model=self.model,
            query=query,
            pagination_params=None,
            sort_params=sort_params,
        )

    def get_by_filter(
        self,
        pagination_params: Optional[PaginationParams] = PaginationParams(),
        sort_params: Optional[SortParams] = SortParams(),
    ) -> Tuple[List[ModelType], MetadataResponse]:
        query = db.session.query(self.model)
        return paginate(
            model=self.model,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )

    def check_duplicate(self, filters: Dict[str, Any]) -> Optional[ModelType]:
        """
        Check if a record with given filters already exists
        """
        query = db.session.query(self.model)
        for key, value in filters.items():
            if value is None:
                continue
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()

    def create(
        self, data: dict[str, Any], duplicate_check: Optional[Dict[str, Any]] = None
    ) -> ModelType:
        """
        Create a new record. If duplicate_check is provided, check for duplicates first.
        """
        if duplicate_check:
            existing = self.check_duplicate(duplicate_check)
            if existing:
                raise CustomException(exception=ExceptionType.DUPLICATE_ENTRY)

        obj_data = jsonable_encoder(data)
        obj = self.model(**obj_data)
        db.session.add(obj)
        self._commit()
        db.session.refresh(obj)
        return obj

    def update_by_id(self, pk_value: Any, data: dict[str, Any]) -> ModelType:
        obj_data = jsonable_encoder(data)
        exist_obj = self.get_by_id(pk_value)
        for field in obj_data:
            setattr(exist_obj, field, obj_data[field])
        self._commit()
        db.session.refresh(exist_obj)
        return exist_obj

    def partial_update_by_id(self, pk_value: Any, data: dict[str, Any]) -> ModelType:
        obj_data = jsonable_encoder(data)
        exist_obj = self.get_by_id(pk_value)
        for field in obj_data:
            if hasattr(exist_obj, field) and obj_data[field] is not None:
                if isinstance(getattr(exist_obj, field), list) and not obj_data[field]:
                    setattr(exist_obj, field, [])
                else:
                    setattr(exist_obj, field, obj_data[field])
        self._commit()
        db.session.refresh(exist_obj)
        return exist_obj

    def delete_by_id(self, pk_value: Any) -> None:
        obj = self.get_by_id(pk_value)
        db.session.delete(obj)
        self._commit()

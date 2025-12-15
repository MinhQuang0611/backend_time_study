from typing import Any, List
from fastapi import APIRouter, Depends, status
from app.utils.exception_handler import CustomException, ExceptionType
from app.schemas.sche_response import DataResponse
from app.schemas.sche_base import PaginationParams, SortParams
from app.schemas.sche_session import (
    SessionCreateRequest,
    SessionUpdateRequest,
    SessionBaseResponse,
    SessionPauseCreateRequest,
    SessionPauseUpdateRequest,
    SessionPauseBaseResponse,
)
from app.services.srv_session import SessionService, SessionPauseService
from app.utils.login_manager import AuthenticateUserEntityRequired
from app.models.model_user_entity import UserEntity

router = APIRouter(prefix=f"/sessions")

session_service: SessionService = SessionService()
session_pause_service: SessionPauseService = SessionPauseService()


# Session endpoints
@router.get(
    "/all",
    response_model=DataResponse[List[SessionBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired())
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        query = db.session.query(SessionEntity).filter(SessionEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=SessionEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "",
    response_model=DataResponse[List[SessionBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        from app.utils.paging import paginate
        query = db.session.query(SessionEntity).filter(SessionEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=SessionEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "",
    response_model=DataResponse[SessionBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create(
    session_data: SessionCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        session_dict = session_data.model_dump()
        session_dict["user_id"] = current_user.user_id
        new_session = session_service.create(data=session_dict)
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/{session_id}",
    response_model=DataResponse[SessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    session_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        session = session_service.get_by_id(session_id)
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=session)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/{session_id}",
    response_model=DataResponse[SessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_by_id(
    session_id: int,
    session_data: SessionUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        session = session_service.get_by_id(session_id)
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_session = session_service.update_by_id(session_id, data=session_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/{session_id}",
    response_model=DataResponse[SessionBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_by_id(
    session_id: int,
    session_data: SessionUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        session = session_service.get_by_id(session_id)
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_session = session_service.partial_update_by_id(session_id, data=session_data.model_dump(exclude_unset=True))
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_session)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(
    session_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        session = session_service.get_by_id(session_id)
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        session_service.delete_by_id(session_id)
    except Exception as e:
        raise CustomException(exception=e)


# Session Pause endpoints
@router.get(
    "/pauses/all",
    response_model=DataResponse[List[SessionPauseBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_all_pauses(
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionPauseEntity, SessionEntity
        from app.utils.paging import paginate
        from app.schemas.sche_base import SortParams
        # Filter by user_id through session
        query = db.session.query(SessionPauseEntity).join(
            SessionEntity, SessionPauseEntity.session_id == SessionEntity.session_id
        ).filter(SessionEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=SessionPauseEntity,
            query=query,
            pagination_params=None,
            sort_params=SortParams(),
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.get(
    "/pauses",
    response_model=DataResponse[List[SessionPauseBaseResponse]],
    status_code=status.HTTP_200_OK,
)
def get_pauses_by_filter(
    sort_params: SortParams = Depends(),
    pagination_params: PaginationParams = Depends(),
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionPauseEntity, SessionEntity
        from app.utils.paging import paginate
        # Filter by user_id through session
        query = db.session.query(SessionPauseEntity).join(
            SessionEntity, SessionPauseEntity.session_id == SessionEntity.session_id
        ).filter(SessionEntity.user_id == current_user.user_id)
        data, metadata = paginate(
            model=SessionPauseEntity,
            query=query,
            pagination_params=pagination_params,
            sort_params=sort_params,
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=data, metadata=metadata)
    except Exception as e:
        return CustomException(exception=e)


@router.post(
    "/pauses",
    response_model=DataResponse[SessionPauseBaseResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_pause(
    pause_data: SessionPauseCreateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        # Verify session belongs to current user
        session = db.session.query(SessionEntity).filter(
            SessionEntity.session_id == pause_data.session_id
        ).first()
        if not session:
            raise CustomException(exception=ExceptionType.NOT_FOUND)
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        new_pause = session_pause_service.create(data=pause_data.model_dump())
        return DataResponse(http_code=status.HTTP_201_CREATED, data=new_pause)
    except Exception as e:
        raise CustomException(exception=e)


@router.get(
    "/pauses/{pause_id}",
    response_model=DataResponse[SessionPauseBaseResponse],
    status_code=status.HTTP_200_OK,
)
def get_pause_by_id(
    pause_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        pause = session_pause_service.get_by_id(pause_id)
        # Verify session belongs to current user
        session = db.session.query(SessionEntity).filter(
            SessionEntity.session_id == pause.session_id
        ).first()
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        return DataResponse(http_code=status.HTTP_200_OK, data=pause)
    except Exception as e:
        raise CustomException(exception=e)


@router.put(
    "/pauses/{pause_id}",
    response_model=DataResponse[SessionPauseBaseResponse],
    status_code=status.HTTP_200_OK,
)
def update_pause_by_id(
    pause_id: int,
    pause_data: SessionPauseUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        pause = session_pause_service.get_by_id(pause_id)
        # Verify session belongs to current user
        session = db.session.query(SessionEntity).filter(
            SessionEntity.session_id == pause.session_id
        ).first()
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_pause = session_pause_service.update_by_id(
            pause_id, data=pause_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_pause)
    except Exception as e:
        raise CustomException(exception=e)


@router.patch(
    "/pauses/{pause_id}",
    response_model=DataResponse[SessionPauseBaseResponse],
    status_code=status.HTTP_200_OK,
)
def partial_update_pause_by_id(
    pause_id: int,
    pause_data: SessionPauseUpdateRequest,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> Any:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        pause = session_pause_service.get_by_id(pause_id)
        # Verify session belongs to current user
        session = db.session.query(SessionEntity).filter(
            SessionEntity.session_id == pause.session_id
        ).first()
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        updated_pause = session_pause_service.partial_update_by_id(
            pause_id, data=pause_data.model_dump(exclude_unset=True)
        )
        return DataResponse(http_code=status.HTTP_200_OK, data=updated_pause)
    except Exception as e:
        raise CustomException(exception=e)


@router.delete(
    "/pauses/{pause_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_pause_by_id(
    pause_id: int,
    current_user: UserEntity = Depends(AuthenticateUserEntityRequired()),
) -> None:
    try:
        from fastapi_sqlalchemy import db
        from app.models.model_session import SessionEntity
        pause = session_pause_service.get_by_id(pause_id)
        # Verify session belongs to current user
        session = db.session.query(SessionEntity).filter(
            SessionEntity.session_id == pause.session_id
        ).first()
        if session.user_id != current_user.user_id:
            raise CustomException(exception=ExceptionType.FORBIDDEN)
        session_pause_service.delete_by_id(pause_id)
    except Exception as e:
        raise CustomException(exception=e)


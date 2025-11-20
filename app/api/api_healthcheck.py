import os

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter

from app.schemas.sche_response import BaseResponse
from app.core.config import settings

router = APIRouter(prefix=f"/health-check")


@router.get("", response_model=BaseResponse)
async def get():
    return BaseResponse(http_code=200, message="OK")

@router.get("/db-check")
def db_check():
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))  # 
        return {"status": "ok", "message": "Connected to database successfully!"}
    except SQLAlchemyError as e:
        return {"status": "failed", "message": str(e)}
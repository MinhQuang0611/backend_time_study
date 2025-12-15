import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.model_external_account import ExternalAccount
from app.models.model_user_entity import UserEntity as User


def link_facebook_account(
    *,
    db: Session,
    user_id: int,
    facebook_id: str,
    name: str | None = None,
    picture: str | None = None,
):
    # 0. Check user tồn tại
    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # 1. Facebook đã được link chưa?
    existing = db.execute(
        select(ExternalAccount).where(
            ExternalAccount.provider == "facebook",
            ExternalAccount.provider_user_id == facebook_id,
        )
    ).scalar_one_or_none()

    if existing and existing.user_id != user_id:
        raise HTTPException(
            status_code=400,
            detail="Facebook account already linked to another user",
        )

    # 2. User này đã link Facebook chưa?
    user_fb = db.execute(
        select(ExternalAccount).where(
            ExternalAccount.user_id == user_id,
            ExternalAccount.provider == "facebook",
        )
    ).scalar_one_or_none()

    if user_fb:
        raise HTTPException(
            status_code=400,
            detail="User already linked Facebook",
        )

    # 3. Link
    fb_account = ExternalAccount(
        user_id=user_id,
        provider="facebook",
        provider_user_id=facebook_id,
        name=name,
        avatar_url=picture,
        created_at=time.time(),
    )

    db.add(fb_account)
    db.commit()
    db.refresh(fb_account)

    return fb_account

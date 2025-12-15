# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.schemas.sche_external_account import (
#     FacebookLinkRequest,
#     FacebookLinkResponse,
# )
# from app.services.srv_external_account import link_facebook_account
# from app.core.database import get_db

# router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.post("/link/facebook", response_model=FacebookLinkResponse)
# def link_facebook(
#     data: FacebookLinkRequest,
#     db: Session = Depends(get_db),
# ):
#     link_facebook_account(
#         db=db,
#         user_id=data.user_id,
#         facebook_id=data.facebook_id,
#         name=data.name,
#         picture=data.picture,
#     )

#     return {"message": "Facebook linked successfully"}

from pydantic import BaseModel, Field

class FacebookLinkRequest(BaseModel):
    # user_id is now obtained from JWT token
    facebook_id: str = Field(..., description="Facebook user id")
    name: str | None = None
    picture: str | None = None


class FacebookLinkResponse(BaseModel):
    message: str

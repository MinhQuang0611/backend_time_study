from pydantic import BaseModel, Field
from typing import List, Optional

class FacebookLinkRequest(BaseModel):
    # user_id is now obtained from JWT token
    facebook_id: str = Field(..., description="Facebook user id")
    name: str | None = None
    picture: str | None = None


class FacebookLinkResponse(BaseModel):
    message: str


class FacebookFriendsRequest(BaseModel):
    access_token: str = Field(..., description="Facebook access token để gọi Graph API")


class FacebookFriendInfo(BaseModel):
    facebook_user_id: str
    name: Optional[str] = None
    picture_url: Optional[str] = None


class FacebookFriendsResponse(BaseModel):
    message: str
    total_friends: int
    total_friends_count: Optional[int] = None  # Tổng số bạn bè thực tế của user
    friends_saved: int
    friends_updated: int = 0  # Số bạn bè đã được cập nhật
    friends: List[FacebookFriendInfo]
    note: Optional[str] = None  # Ghi chú về hạn chế của Facebook API

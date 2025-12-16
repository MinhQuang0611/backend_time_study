import time
import requests
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Dict, Any

from app.models.model_external_account import ExternalAccount
from app.models.model_user_entity import UserEntity as User
from app.models.model_facebook_friend import FacebookFriend


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


def sync_facebook_friends(
    *,
    db: Session,
    user_id: int,
    access_token: str,
) -> Dict[str, Any]:
    """
    Gọi Facebook Graph API để lấy danh sách bạn bè và lưu vào database.
    
    Args:
        db: Database session
        user_id: ID của user
        access_token: Facebook access token
        
    Returns:
        Dict chứa thông tin về số lượng bạn bè đã lưu
    """
    # 0. Check user tồn tại
    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # 1. Lấy thông tin user trước để kiểm tra
    try:
        me_response = requests.get(
            "https://graph.facebook.com/v19.0/me",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"fields": "id,name,friends.summary(true)"}
        )
        me_response.raise_for_status()
        me_data = me_response.json()
        total_friends_count = me_data.get("friends", {}).get("summary", {}).get("total_count", 0)
        print(f"========== FACEBOOK USER INFO ==========", flush=True)
        print(f"User ID: {me_data.get('id')}", flush=True)
        print(f"User Name: {me_data.get('name')}", flush=True)
        print(f"Total Friends (from summary): {total_friends_count}", flush=True)
        print("========================================", flush=True)
    except Exception as e:
        print(f"Warning: Could not fetch user info: {str(e)}", flush=True)
        total_friends_count = 0
    
    # 2. Gọi Facebook Graph API để lấy danh sách bạn bè
    # LƯU Ý: API /me/friends chỉ trả về những bạn bè ĐÃ CÀI ĐẶT VÀ CẤP QUYỀN cho cùng app
    # Đây là chính sách bảo vệ quyền riêng tư của Facebook từ năm 2015
    url = "https://graph.facebook.com/v19.0/me/friends"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "fields": "id,name,picture.type(large)",
        "limit": 100  # Facebook API limit
    }
    
    all_friends = []
    next_url = url
    
    try:
        # Xử lý pagination nếu có
        while next_url:
            response = requests.get(
                next_url,
                headers=headers,
                params=params if next_url == url else None
            )
            response.raise_for_status()
            
            data = response.json()
            friends_data = data.get("data", [])
            all_friends.extend(friends_data)
            
            print(f"Fetched {len(friends_data)} friends in this page", flush=True)
            
            # Kiểm tra xem có trang tiếp theo không
            paging = data.get("paging", {})
            next_url = paging.get("next")
            if next_url:
                # Nếu có next URL, không cần params nữa vì URL đã có đầy đủ
                params = None
                
    except requests.exceptions.HTTPError as e:
        error_data = {}
        try:
            error_data = e.response.json()
        except:
            pass
        
        error_message = error_data.get("error", {}).get("message", str(e))
        error_code = error_data.get("error", {}).get("code", 0)
        
        print(f"========== FACEBOOK API ERROR ==========", flush=True)
        print(f"Error code: {error_code}", flush=True)
        print(f"Error message: {error_message}", flush=True)
        print(f"Response: {error_data}", flush=True)
        print("=========================================", flush=True)
        
        raise HTTPException(
            status_code=400,
            detail=f"Facebook API error: {error_message}"
        )
    except Exception as e:
        print(f"========== UNEXPECTED ERROR ==========", flush=True)
        print(f"Error: {str(e)}", flush=True)
        print("=======================================", flush=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
    
    print(f"========== FACEBOOK FRIENDS FETCHED ==========", flush=True)
    print(f"Total friends from API: {len(all_friends)}", flush=True)
    if total_friends_count > 0:
        print(f"User's total friends count: {total_friends_count}", flush=True)
        print(f"Friends using this app: {len(all_friends)}", flush=True)
        print(f"Note: /me/friends only returns friends who have installed and granted permissions to this app", flush=True)
    print("===============================================", flush=True)
    
    # Cảnh báo nếu không có bạn bè nào
    if len(all_friends) == 0 and total_friends_count > 0:
        print("WARNING: No friends returned, but user has friends.", flush=True)
        print("This is normal - only friends who installed this app will appear.", flush=True)
    
    # 2. Lưu bạn bè vào database
    friends_saved = 0
    friends_list = []
    
    for friend_data in all_friends:
        facebook_user_id = friend_data.get("id")
        name = friend_data.get("name")
        picture_data = friend_data.get("picture", {})
        picture_url = picture_data.get("data", {}).get("url") if picture_data else None
        
        if not facebook_user_id:
            continue
        
        # Kiểm tra xem bạn bè này đã tồn tại chưa
        existing_friend = db.execute(
            select(FacebookFriend).where(
                FacebookFriend.user_id == user_id,
                FacebookFriend.facebook_user_id == facebook_user_id
            )
        ).scalar_one_or_none()
        
        if existing_friend:
            # Update thông tin nếu có thay đổi
            if name and existing_friend.name != name:
                existing_friend.name = name
            if picture_url and existing_friend.picture_url != picture_url:
                existing_friend.picture_url = picture_url
            db.commit()
            friends_list.append({
                "facebook_user_id": facebook_user_id,
                "name": existing_friend.name,
                "picture_url": existing_friend.picture_url
            })
        else:
            # Tạo bạn bè mới
            new_friend = FacebookFriend(
                user_id=user_id,
                facebook_user_id=facebook_user_id,
                name=name,
                picture_url=picture_url,
            )
            db.add(new_friend)
            friends_saved += 1
            friends_list.append({
                "facebook_user_id": facebook_user_id,
                "name": name,
                "picture_url": picture_url
            })
    
    db.commit()
    
    print(f"========== FACEBOOK FRIENDS SAVED ==========", flush=True)
    print(f"New friends saved: {friends_saved}", flush=True)
    print(f"Total friends in DB: {len(friends_list)}", flush=True)
    print("==============================================", flush=True)
    
    message = "Facebook friends synced successfully"
    if len(all_friends) == 0:
        message += ". Note: Only friends who have installed and granted permissions to this app are returned by Facebook API."
    
    return {
        "message": message,
        "total_friends": len(all_friends),
        "total_friends_count": total_friends_count if total_friends_count > 0 else None,
        "friends_saved": friends_saved,
        "friends": friends_list,
        "note": "Facebook API /me/friends only returns friends who have installed this app. This is Facebook's privacy policy since 2015."
    }

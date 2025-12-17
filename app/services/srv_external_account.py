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
        # Nếu đã có, update với Facebook ID mới (có thể đang là Firebase UID)
        print(f"Updating existing external_account: {user_fb.provider_user_id} -> {facebook_id}", flush=True)
        user_fb.provider_user_id = facebook_id
        if name:
            user_fb.name = name
        if picture:
            user_fb.avatar_url = picture
        db.commit()
        db.refresh(user_fb)
        return user_fb

    # 3. Link mới
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
    total_friends_count = 0
    try:
        me_response = requests.get(
            "https://graph.facebook.com/v19.0/me",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"fields": "id,name,friends.summary(true)"}
        )
        me_response.raise_for_status()
        me_data = me_response.json()
        total_friends_count = me_data.get("friends", {}).get("summary", {}).get("total_count", 0)
        facebook_user_id = me_data.get("id")  # Facebook ID thực sự của user
        print(f"========== FACEBOOK USER INFO ==========", flush=True)
        print(f"User ID: {facebook_user_id}", flush=True)
        print(f"User Name: {me_data.get('name')}", flush=True)
        print(f"Total Friends (from summary): {total_friends_count}", flush=True)
        print("========================================", flush=True)
        
        # Update external_account với Facebook ID thực sự nếu có
        if facebook_user_id:
            from app.models.model_external_account import ExternalAccount
            user_fb_account = db.execute(
                select(ExternalAccount).where(
                    ExternalAccount.user_id == user_id,
                    ExternalAccount.provider == "facebook"
                )
            ).scalar_one_or_none()
            
            if user_fb_account:
                # Nếu provider_user_id là Firebase UID (dài hơn 20 ký tự) hoặc khác Facebook ID
                if len(user_fb_account.provider_user_id) > 20 or user_fb_account.provider_user_id != str(facebook_user_id):
                    print(f"Updating external_account: {user_fb_account.provider_user_id} -> {facebook_user_id}", flush=True)
                    user_fb_account.provider_user_id = str(facebook_user_id)
                    db.commit()
                    print(f"Updated external_account with Facebook ID: {facebook_user_id}", flush=True)
            else:
                # Nếu chưa có external_account, tạo mới
                print(f"Creating new external_account with Facebook ID: {facebook_user_id}", flush=True)
                fb_account = ExternalAccount(
                    user_id=user_id,
                    provider="facebook",
                    provider_user_id=str(facebook_user_id),
                    name=me_data.get("name"),
                    avatar_url=None,
                    created_at=time.time(),
                )
                db.add(fb_account)
                db.commit()
                print(f"Created external_account with Facebook ID: {facebook_user_id}", flush=True)
    except Exception as e:
        print(f"Warning: Could not fetch user info: {str(e)}", flush=True)
        # Không raise error, tiếp tục với việc lấy friends
    
    # 2. Gọi Facebook Graph API để lấy danh sách bạn bè
    # LƯU Ý: API /me/friends chỉ trả về những bạn bè ĐÃ CÀI ĐẶT VÀ CẤP QUYỀN cho cùng app
    # Đây là chính sách bảo vệ quyền riêng tư của Facebook từ năm 2015
    base_url = "https://graph.facebook.com/v19.0/me/friends"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "fields": "id,name,picture.type(large)",
        "limit": 100  # Facebook API limit
    }
    
    all_friends = []
    after_cursor = None
    
    try:
        # Xử lý pagination với cursors
        while True:
            # Thêm cursor vào params nếu có
            current_params = params.copy()
            if after_cursor:
                current_params["after"] = after_cursor
            
            response = requests.get(
                base_url,
                headers=headers,
                params=current_params,
                timeout=30  # Timeout 30 giây
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Lấy danh sách bạn bè từ data
            friends_data = data.get("data", [])
            if not isinstance(friends_data, list):
                friends_data = []
            
            print(f"Fetched {len(friends_data)} friends in this page", flush=True)
            
            # Xử lý từng bạn bè
            for friend in friends_data:
                if not isinstance(friend, dict):
                    continue
                    
                friend_id = friend.get("id")
                if not friend_id:
                    continue
                
                # Chuẩn hóa dữ liệu bạn bè
                normalized_friend = {
                    "id": str(friend_id),  # Đảm bảo là string
                    "name": friend.get("name", ""),
                    "picture": None
                }
                
                # Lấy picture nếu có
                picture_data = friend.get("picture")
                if picture_data and isinstance(picture_data, dict):
                    picture_info = picture_data.get("data", {})
                    if isinstance(picture_info, dict):
                        normalized_friend["picture"] = picture_info.get("url")
                
                # Nếu không có picture, tạo URL từ Facebook ID
                if not normalized_friend["picture"]:
                    normalized_friend["picture"] = f"https://graph.facebook.com/{friend_id}/picture?type=large"
                
                all_friends.append(normalized_friend)
            
            # Kiểm tra pagination với cursors
            paging = data.get("paging", {})
            if not paging or not isinstance(paging, dict):
                break
                
            cursors = paging.get("cursors", {})
            if not cursors or not isinstance(cursors, dict):
                break
                
            after_cursor = cursors.get("after")
            if not after_cursor:
                break
                
            print(f"Fetching next page with cursor: {after_cursor[:20]}...", flush=True)
                
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
    
    # 3. Lưu bạn bè vào database
    friends_saved = 0
    friends_updated = 0
    friends_list = []
    
    print(f"========== SAVING FRIENDS TO DATABASE ==========", flush=True)
    print(f"Total friends to process: {len(all_friends)}", flush=True)
    
    for friend_data in all_friends:
        try:
            facebook_user_id = friend_data.get("id")
            name = friend_data.get("name") or ""
            picture_url = friend_data.get("picture") or ""
            
            # Validate facebook_user_id
            if not facebook_user_id or not str(facebook_user_id).strip():
                print(f"Skipping friend with invalid ID: {friend_data}", flush=True)
                continue
            
            facebook_user_id = str(facebook_user_id).strip()
            
            # Kiểm tra xem bạn bè này đã tồn tại chưa
            existing_friend = db.execute(
                select(FacebookFriend).where(
                    FacebookFriend.user_id == user_id,
                    FacebookFriend.facebook_user_id == facebook_user_id
                )
            ).scalar_one_or_none()
            
            if existing_friend:
                # Update thông tin nếu có thay đổi
                updated = False
                if name and existing_friend.name != name:
                    existing_friend.name = name
                    updated = True
                if picture_url and existing_friend.picture_url != picture_url:
                    existing_friend.picture_url = picture_url
                    updated = True
                
                if updated:
                    friends_updated += 1
                    db.commit()
                
                friends_list.append({
                    "facebook_user_id": facebook_user_id,
                    "name": existing_friend.name or name,
                    "picture_url": existing_friend.picture_url or picture_url
                })
            else:
                # Tạo bạn bè mới
                try:
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
                except Exception as db_error:
                    print(f"Error saving friend {facebook_user_id}: {str(db_error)}", flush=True)
                    db.rollback()
                    continue
        except Exception as e:
            print(f"Error processing friend: {str(e)}", flush=True)
            print(f"Friend data: {friend_data}", flush=True)
            continue
    
    try:
        db.commit()
        print(f"Database commit successful", flush=True)
    except Exception as e:
        print(f"Error committing to database: {str(e)}", flush=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    
    print(f"========== FACEBOOK FRIENDS SAVED ==========", flush=True)
    print(f"New friends saved: {friends_saved}", flush=True)
    print(f"Friends updated: {friends_updated}", flush=True)
    print(f"Total friends in response: {len(friends_list)}", flush=True)
    print("==============================================", flush=True)
    
    message = "Facebook friends synced successfully"
    if len(all_friends) == 0:
        message += ". Note: Only friends who have installed and granted permissions to this app are returned by Facebook API."
    
    return {
        "message": message,
        "total_friends": len(all_friends),
        "total_friends_count": total_friends_count if total_friends_count > 0 else None,
        "friends_saved": friends_saved,
        "friends_updated": friends_updated,
        "friends": friends_list,
        "note": "Facebook API /me/friends only returns friends who have installed this app. This is Facebook's privacy policy since 2015."
    }


def migrate_external_accounts_to_facebook_ids(
    *,
    db: Session,
) -> Dict[str, Any]:
    """
    Migration function: Tự động update tất cả external_accounts từ Firebase UID sang Facebook ID thực sự.
    
    Logic:
    1. Tìm tất cả external_accounts có provider='facebook' và provider_user_id là Firebase UID (dài > 20 ký tự)
    2. Với mỗi user, extract Facebook ID từ profile_picture_url nếu có dạng https://graph.facebook.com/{facebook_id}/picture
    3. Update external_account với Facebook ID đó
    
    Args:
        db: Database session
        
    Returns:
        Dict chứa thông tin về số lượng accounts đã update
    """
    import re
    
    print("========== MIGRATING EXTERNAL ACCOUNTS ==========", flush=True)
    
    # 1. Tìm tất cả external_accounts có provider='facebook' và provider_user_id là Firebase UID
    all_external_accounts = db.execute(
        select(ExternalAccount).where(
            ExternalAccount.provider == "facebook"
        )
    ).scalars().all()
    
    print(f"Found {len(all_external_accounts)} Facebook external accounts", flush=True)
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    updated_details = []
    
    for ext_account in all_external_accounts:
        try:
            provider_user_id = ext_account.provider_user_id
            
            # Kiểm tra xem có phải Firebase UID không (dài > 20 ký tự, không phải số thuần)
            is_firebase_uid = len(provider_user_id) > 20 or not provider_user_id.isdigit()
            
            if not is_firebase_uid:
                # Đã là Facebook ID rồi, skip
                skipped_count += 1
                continue
            
            # 2. Lấy user để extract Facebook ID từ profile_picture_url
            user = db.execute(
                select(User).where(User.user_id == ext_account.user_id)
            ).scalar_one_or_none()
            
            if not user:
                print(f"User {ext_account.user_id} not found, skipping", flush=True)
                skipped_count += 1
                continue
            
            facebook_id = None
            
            # Extract từ profile_picture_url: https://graph.facebook.com/{facebook_id}/picture
            if user.profile_picture_url:
                match = re.search(r'graph\.facebook\.com/(\d+)/picture', user.profile_picture_url)
                if match:
                    facebook_id = match.group(1)
                    print(f"Extracted Facebook ID from profile_picture_url: {facebook_id}", flush=True)
            
            # Nếu không tìm được từ profile_picture_url, tìm trong facebook_friends
            # Tìm xem có user nào khác đã sync friends và có facebook_user_id match với user này không
            if not facebook_id:
                # Tìm trong facebook_friends của chính user này (nếu có ai đã sync friends với user này)
                # Nhưng đây là bạn bè của họ, không phải ID của họ
                # Tìm trong tất cả facebook_friends xem có facebook_user_id nào đã có external_account với Facebook ID thực sự chưa
                # Điều này phức tạp, tôi sẽ bỏ qua
                pass
            
            if not facebook_id:
                print(f"Could not extract Facebook ID for user {ext_account.user_id}, skipping", flush=True)
                skipped_count += 1
                continue
            
            # 3. Kiểm tra xem Facebook ID này đã được sử dụng bởi user khác chưa
            existing_account = db.execute(
                select(ExternalAccount).where(
                    ExternalAccount.provider == "facebook",
                    ExternalAccount.provider_user_id == facebook_id,
                    ExternalAccount.user_id != ext_account.user_id
                )
            ).scalar_one_or_none()
            
            if existing_account:
                print(f"Facebook ID {facebook_id} already used by user {existing_account.user_id}, skipping user {ext_account.user_id}", flush=True)
                skipped_count += 1
                continue
            
            # 4. Update external_account với Facebook ID
            old_provider_user_id = ext_account.provider_user_id
            ext_account.provider_user_id = facebook_id
            db.commit()
            
            updated_count += 1
            updated_details.append({
                "user_id": ext_account.user_id,
                "old_provider_user_id": old_provider_user_id,
                "new_facebook_id": facebook_id,
                "user_email": user.email,
                "user_display_name": user.display_name
            })
            
            print(f"Updated user {ext_account.user_id}: {old_provider_user_id} -> {facebook_id}", flush=True)
            
        except Exception as e:
            print(f"Error processing external_account {ext_account.external_account_id}: {str(e)}", flush=True)
            error_count += 1
            db.rollback()
            continue
    
    print("================================================", flush=True)
    print(f"Migration completed:", flush=True)
    print(f"  - Updated: {updated_count}", flush=True)
    print(f"  - Skipped: {skipped_count}", flush=True)
    print(f"  - Errors: {error_count}", flush=True)
    print("================================================", flush=True)
    
    return {
        "message": "Migration completed",
        "updated_count": updated_count,
        "skipped_count": skipped_count,
        "error_count": error_count,
        "updated_details": updated_details
    }

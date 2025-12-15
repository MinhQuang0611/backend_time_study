# API Documentation

## Base URL
```
http://localhost:8669/api
```

## Authentication

Tất cả các API (trừ auth endpoints) yêu cầu JWT Bearer token trong header:

```
Authorization: Bearer <access_token>
```

---

## 📋 Mục lục

1. [Authentication APIs](#authentication-apis)
2. [User Entity APIs](#user-entity-apis)
3. [Task APIs](#task-apis)
4. [Session APIs](#session-apis)
5. [Goal APIs](#goal-apis)
6. [Setting APIs](#setting-apis)
7. [Statistics APIs](#statistics-apis)
8. [Error Handling](#error-handling)
9. [Pagination & Sorting](#pagination--sorting)

---

## 🔐 Authentication APIs

Base path: `/auth/user-entity`

### 1. Đăng ký tài khoản

**Endpoint:** `POST /auth/user-entity/register`

**Authentication:** Không cần

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123",
  "display_name": "Nguyễn Văn A",
  "profile_picture_url": "https://example.com/avatar.jpg"
}
```

**Response (201 Created):**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "data": {
    "user_id": 1,
    "email": "user@example.com",
    "display_name": "Nguyễn Văn A",
    "profile_picture_url": "https://example.com/avatar.jpg",
    "created_at": 1703123456.789,
    "last_login": null,
    "is_anonymous": 0,
    "updated_at": 1703123456.789
  },
  "metadata": null
}
```

**Validation Rules:**
- `email`: Bắt buộc, định dạng email hợp lệ
- `password`: Bắt buộc, tối thiểu 8 ký tự, không được chỉ có số
- `display_name`: Tùy chọn, tối đa 255 ký tự
- `profile_picture_url`: Tùy chọn, tối đa 1024 ký tự

---

### 2. Đăng nhập với Email/Password

**Endpoint:** `POST /auth/user-entity/login`

**Authentication:** Không cần

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

**Response (200 OK):**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": null,
    "expires_in": 604800,
    "refresh_expires_in": 604800,
    "token_type": "Bearer",
    "user": {
      "user_id": 1,
      "email": "user@example.com",
      "display_name": "Nguyễn Văn A",
      "profile_picture_url": "https://example.com/avatar.jpg",
      "created_at": 1703123456.789,
      "last_login": 1703123456.789,
      "is_anonymous": 0,
      "updated_at": 1703123456.789
    }
  },
  "metadata": null
}
```

**Error Messages:**
- `401`: "Email và mật khẩu không được để trống"
- `401`: "Tài khoản không tồn tại"
- `401`: "Tài khoản này chưa được thiết lập mật khẩu. Vui lòng đăng nhập bằng phương thức khác hoặc đặt lại mật khẩu."
- `401`: "Email hoặc mật khẩu không đúng"

---

### 3. Đăng nhập với Firebase ID Token

**Endpoint:** `POST /auth/user-entity/login-firebase`

**Authentication:** Không cần

**Mô tả:** 
- Đăng nhập/đăng ký với Firebase (hỗ trợ Facebook, Google, Email)
- Tự động tạo user mới nếu chưa tồn tại
- Tự động link Facebook account nếu login qua Facebook

**Request Body:**
```json
{
  "firebase_id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ij..."
}
```

**Response (200 OK):**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 604800,
    "refresh_expires_in": 2592000,
    "token_type": "Bearer",
    "user": {
      "user_id": 1,
      "email": "user@example.com",
      "display_name": "Nguyễn Văn A",
      "profile_picture_url": "https://example.com/avatar.jpg",
      "created_at": 1703123456.789,
      "last_login": 1703123456.789,
      "is_anonymous": 0,
      "updated_at": 1703123456.789
    }
  },
  "metadata": null
}
```

**Luồng xử lý:**
1. Verify Firebase ID Token với Firebase Admin SDK
2. Lấy thông tin user từ token (uid, email, name, picture)
3. Tìm user theo email (nếu có)
4. Nếu chưa có → Tự động tạo UserEntity mới
5. Nếu login qua Facebook → Tự động tạo ExternalAccount để link Facebook
6. Tạo Access Token (7 ngày) và Refresh Token (30 ngày)
7. Trả về tokens và user info

---

### 4. Refresh Access Token

**Endpoint:** `POST /auth/user-entity/refresh-token`

**Authentication:** Không cần

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 604800,
    "refresh_expires_in": 2592000,
    "token_type": "Bearer",
    "user": {
      "user_id": 1,
      "email": "user@example.com",
      "display_name": "Nguyễn Văn A",
      "profile_picture_url": "https://example.com/avatar.jpg",
      "created_at": 1703123456.789,
      "last_login": 1703123456.789,
      "is_anonymous": 0,
      "updated_at": 1703123456.789
    }
  },
  "metadata": null
}
```

**Lưu ý:** 
- Refresh token được rotate (tạo mới) mỗi lần refresh
- Access token hết hạn sau 7 ngày
- Refresh token hết hạn sau 30 ngày

---

### 5. Link Facebook Account

**Endpoint:** `POST /auth/user-entity/link/facebook`

**Authentication:** ✅ Cần (Bearer token)

**Mô tả:** Link tài khoản Facebook với user đang đăng nhập

**Request Body:**
```json
{
  "facebook_id": "123456789",
  "name": "Nguyễn Văn A",
  "picture": "https://graph.facebook.com/123456789/picture"
}
```

**Response (200 OK):**
```json
{
  "message": "Facebook linked successfully"
}
```

**Error Messages:**
- `400`: "Facebook account already linked to another user"
- `400`: "User already linked Facebook"
- `404`: "User not found"

---

## 👤 User Entity APIs

Base path: `/v1/user-entities`

**Lưu ý:** Các API này không tự động filter theo user_id. Cần kiểm tra quyền truy cập nếu cần.

### 1. Lấy danh sách tất cả users

**Endpoint:** `GET /v1/user-entities/all`

### 2. Lấy danh sách với filter và pagination

**Endpoint:** `GET /v1/user-entities`

**Query Parameters:** Tương tự các API khác (page, page_size, sort_by, order)

### 3. Tạo user mới

**Endpoint:** `POST /v1/user-entities`

**Request Body:**
```json
{
  "email": "user@example.com",
  "display_name": "Nguyễn Văn A",
  "profile_picture_url": "https://example.com/avatar.jpg",
  "is_anonymous": 0
}
```

### 4. Lấy thông tin user theo ID

**Endpoint:** `GET /v1/user-entities/{user_id}`

**Path Parameters:**
- `user_id` (integer, required): ID của user

### 5. Cập nhật thông tin user

**Endpoint:** `PUT /v1/user-entities/{user_id}`

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "display_name": "Tên mới",
  "profile_picture_url": "https://example.com/new-avatar.jpg"
}
```

### 6. Cập nhật một phần user

**Endpoint:** `PATCH /v1/user-entities/{user_id}`

### 7. Xóa user

**Endpoint:** `DELETE /v1/user-entities/{user_id}`

**Response:** `204 No Content`

---

## 📝 Task APIs

Base path: `/v1/tasks`

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

### 1. Lấy danh sách tất cả tasks

**Endpoint:** `GET /v1/tasks/all`

**Response (200 OK):**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "data": [
    {
      "task_id": 1,
      "user_id": 1,
      "title": "Hoàn thành dự án",
      "description": "Làm xong tính năng ABC",
      "priority": "HIGH",
      "task_date": 1703123456.789,
      "is_completed": 0,
      "completed_at": null,
      "total_time_spent": 120,
      "estimated_sessions": 5,
      "actual_sessions": 3,
      "order_index": 0,
      "created_at": 1703123456.789,
      "updated_at": 1703123456.789
    }
  ],
  "metadata": {
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  }
}
```

### 2. Lấy danh sách tasks với filter và pagination

**Endpoint:** `GET /v1/tasks`

**Query Parameters:**
- `page` (integer, optional): Số trang (mặc định: 1)
- `page_size` (integer, optional): Số items mỗi trang (mặc định: 10)
- `sort_by` (string, optional): Trường để sort (mặc định: "created_at")
- `sort_order` (string, optional): "asc" hoặc "desc" (mặc định: "desc")

**Example:**
```
GET /v1/tasks?page=1&page_size=20&sort_by=task_date&sort_order=asc
```

### 3. Tạo task mới

**Endpoint:** `POST /v1/tasks`

**Request Body:**
```json
{
  "title": "Hoàn thành dự án",
  "description": "Làm xong tính năng ABC",
  "priority": "HIGH",
  "task_date": 1703123456.789,
  "is_completed": 0,
  "estimated_sessions": 5
}
```

**Lưu ý:** `user_id` được tự động lấy từ JWT token, không cần gửi trong request

**Response (201 Created):**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "data": {
    "task_id": 1,
    "user_id": 1,
    "title": "Hoàn thành dự án",
    "description": "Làm xong tính năng ABC",
    "priority": "HIGH",
    "task_date": 1703123456.789,
    "is_completed": 0,
    "completed_at": null,
    "total_time_spent": 0,
    "estimated_sessions": 5,
    "actual_sessions": 0,
    "order_index": 0,
    "created_at": 1703123456.789,
    "updated_at": 1703123456.789
  },
  "metadata": null
}
```

### 4. Lấy thông tin task theo ID

**Endpoint:** `GET /v1/tasks/{task_id}`

**Lưu ý:** Chỉ trả về task nếu thuộc về user đang đăng nhập, nếu không → 403 Forbidden

### 5. Cập nhật task

**Endpoint:** `PUT /v1/tasks/{task_id}`

**Request Body:**
```json
{
  "title": "Tiêu đề mới",
  "description": "Mô tả mới",
  "priority": "MEDIUM",
  "is_completed": 1,
  "completed_at": 1703123456.789
}
```

### 6. Cập nhật một phần task

**Endpoint:** `PATCH /v1/tasks/{task_id}`

**Request Body:**
```json
{
  "is_completed": 1
}
```

### 7. Xóa task

**Endpoint:** `DELETE /v1/tasks/{task_id}`

**Response:** `204 No Content`

### Task Session APIs

**Tất cả endpoints đều yêu cầu authentication**

#### 1. Lấy danh sách task sessions

**Endpoint:** `GET /v1/tasks/sessions/all`

#### 2. Lấy danh sách với filter

**Endpoint:** `GET /v1/tasks/sessions`

#### 3. Tạo task session mới

**Endpoint:** `POST /v1/tasks/sessions`

**Request Body:**
```json
{
  "task_id": 1,
  "session_id": 1,
  "time_spent": 25,
  "notes": "Hoàn thành task A"
}
```

#### 4. Cập nhật task session

**Endpoint:** `PUT /v1/tasks/sessions/{task_session_id}`

#### 5. Xóa task session

**Endpoint:** `DELETE /v1/tasks/sessions/{task_session_id}`

---

## 🎯 Session APIs

Base path: `/v1/sessions`

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

### 1. Lấy danh sách tất cả sessions

**Endpoint:** `GET /v1/sessions/all`

### 2. Lấy danh sách sessions với filter và pagination

**Endpoint:** `GET /v1/sessions`

**Query Parameters:** Tương tự Task APIs

### 3. Tạo session mới

**Endpoint:** `POST /v1/sessions`

**Request Body:**
```json
{
  "session_date": 1703123456.789,
  "start_time": 1703123456.789,
  "end_time": 1703123600.789,
  "duration_minutes": 25,
  "actual_duration_minutes": 24,
  "session_type": "FOCUS_SESSION",
  "status": "COMPLETED",
  "focus_session_count": 1,
  "is_completed": 1,
  "pause_count": 0,
  "total_pause_duration": 0
}
```

**Session Types:**
- `FOCUS_SESSION`: Phiên tập trung
- `SHORT_BREAK`: Nghỉ ngắn
- `LONG_BREAK`: Nghỉ dài

**Status:**
- `IN_PROGRESS`: Đang diễn ra
- `COMPLETED`: Hoàn thành
- `PAUSED`: Tạm dừng
- `CANCELLED`: Đã hủy

**Lưu ý:** `user_id` được tự động lấy từ JWT token

### 4. Lấy thông tin session theo ID

**Endpoint:** `GET /v1/sessions/{session_id}`

### 5. Cập nhật session

**Endpoint:** `PUT /v1/sessions/{session_id}`

### 6. Xóa session

**Endpoint:** `DELETE /v1/sessions/{session_id}`

### Session Pause APIs

**Tất cả endpoints đều yêu cầu authentication**

#### 1. Lấy danh sách pauses

**Endpoint:** `GET /v1/sessions/pauses/all`

#### 2. Lấy danh sách với filter

**Endpoint:** `GET /v1/sessions/pauses`

#### 3. Tạo pause mới

**Endpoint:** `POST /v1/sessions/pauses`

**Request Body:**
```json
{
  "session_id": 1,
  "pause_start": 1703123456.789,
  "pause_end": 1703123600.789,
  "pause_duration": 2
}
```

#### 4. Cập nhật pause

**Endpoint:** `PUT /v1/sessions/pauses/{pause_id}`

#### 5. Xóa pause

**Endpoint:** `DELETE /v1/sessions/pauses/{pause_id}`

---

## 🎯 Goal APIs

Base path: `/v1/goals`

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

### 1. Lấy danh sách tất cả goals

**Endpoint:** `GET /v1/goals/all`

### 2. Tạo goal mới

**Endpoint:** `POST /v1/goals`

**Request Body:**
```json
{
  "goal_date": 1703123456.789,
  "target_sessions": 10,
  "completed_sessions": 0,
  "completion_percentage": 0,
  "is_achieved": 0
}
```

**Lưu ý:** `user_id` được tự động lấy từ JWT token

### 3. Cập nhật goal

**Endpoint:** `PUT /v1/goals/{goal_id}`

### 4. Xóa goal

**Endpoint:** `DELETE /v1/goals/{goal_id}`

---

## ⚙️ Setting APIs

Base path: `/v1/settings`

### User Settings

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

#### 1. Lấy danh sách user settings

**Endpoint:** `GET /v1/settings/user/all`

#### 2. Tạo user setting mới

**Endpoint:** `POST /v1/settings/user`

**Request Body:**
```json
{
  "setting_key": "theme",
  "setting_value": "dark",
  "data_type": "STRING"
}
```

**Data Types:**
- `STRING`: Chuỗi
- `INTEGER`: Số nguyên
- `BOOLEAN`: Boolean
- `JSON`: JSON object

**Lưu ý:** `user_id` được tự động lấy từ JWT token

#### 3. Cập nhật user setting

**Endpoint:** `PUT /v1/settings/user/{setting_id}`

#### 4. Xóa user setting

**Endpoint:** `DELETE /v1/settings/user/{setting_id}`

### Default Settings

**Không yêu cầu authentication** (settings chung của hệ thống)

#### 1. Lấy danh sách default settings

**Endpoint:** `GET /v1/settings/default/all`

---

## 📊 Statistics APIs

Base path: `/v1/statistics`

### Statistics Cache

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

#### 1. Lấy danh sách statistics cache

**Endpoint:** `GET /v1/statistics/cache/all`

#### 2. Lấy danh sách với filter và pagination

**Endpoint:** `GET /v1/statistics/cache`

**Query Parameters:** Tương tự các API khác (page, page_size, sort_by, order)

#### 3. Tạo statistics cache mới

**Endpoint:** `POST /v1/statistics/cache`

**Request Body:**
```json
{
  "user_id": 1,
  "stat_date": 1703123456.789,
  "total_sessions": 10,
  "total_focus_time": 300,
  "total_breaks": 5,
  "average_session_duration": 25,
  "longest_session": 45,
  "completed_tasks": 8,
  "total_tasks": 10
}
```

**Lưu ý:** `user_id` được tự động lấy từ JWT token

#### 4. Lấy thông tin statistics cache theo ID

**Endpoint:** `GET /v1/statistics/cache/{cache_id}`

#### 5. Cập nhật statistics cache

**Endpoint:** `PUT /v1/statistics/cache/{cache_id}`

#### 6. Xóa statistics cache

**Endpoint:** `DELETE /v1/statistics/cache/{cache_id}`

### Streak Records

**Tất cả endpoints đều yêu cầu authentication và tự động filter theo user_id từ JWT token**

#### 1. Lấy danh sách streak records

**Endpoint:** `GET /v1/statistics/streak/all`

#### 2. Lấy danh sách với filter và pagination

**Endpoint:** `GET /v1/statistics/streak`

#### 3. Tạo streak record mới

**Endpoint:** `POST /v1/statistics/streak`

**Request Body:**
```json
{
  "user_id": 1,
  "streak_date": 1703123456.789,
  "current_streak": 5,
  "longest_streak": 10,
  "is_active": 1
}
```

**Lưu ý:** `user_id` được tự động lấy từ JWT token

#### 4. Lấy thông tin streak record theo ID

**Endpoint:** `GET /v1/statistics/streak/{streak_id}`

#### 5. Cập nhật streak record

**Endpoint:** `PUT /v1/statistics/streak/{streak_id}`

#### 6. Xóa streak record

**Endpoint:** `DELETE /v1/statistics/streak/{streak_id}`

---

## 📄 Pagination & Sorting

### Query Parameters

Tất cả các API GET với filter đều hỗ trợ pagination và sorting:

**Pagination:**
- `page` (integer, optional): Số trang, mặc định: 1, phải > 0
- `page_size` (integer, optional): Số items mỗi trang, mặc định: 10, tối đa: 100, phải > 0

**Sorting:**
- `sort_by` (string, optional): Trường để sort, mặc định: "id"
- `order` (string, optional): "asc" hoặc "desc", mặc định: "desc"

**Example:**
```
GET /v1/tasks?page=1&page_size=20&sort_by=task_date&order=asc
```

### Response Metadata

```json
{
  "metadata": {
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

---

## ❌ Error Handling

### Error Response Format

```json
{
  "http_code": 401,
  "success": false,
  "message": "Unauthorized",
  "metadata": null
}
```

### HTTP Status Codes

- `200 OK`: Request thành công
- `201 Created`: Tạo mới thành công
- `204 No Content`: Xóa thành công
- `400 Bad Request`: Dữ liệu request không hợp lệ
- `401 Unauthorized`: Chưa đăng nhập hoặc token không hợp lệ
- `403 Forbidden`: Không có quyền truy cập (ví dụ: truy cập resource của user khác)
- `404 Not Found`: Resource không tồn tại
- `409 Conflict`: Resource đã tồn tại (ví dụ: email đã được đăng ký)
- `422 Unvalidation Error`: Validation error
- `500 Internal Server Error`: Lỗi server

### Common Error Messages

**Authentication:**
- `"Unauthorized"`: Token không hợp lệ hoặc đã hết hạn
- `"Email và mật khẩu không được để trống"`
- `"Tài khoản không tồn tại"`
- `"Email hoặc mật khẩu không đúng"`

**Authorization:**
- `"Don't have access rights to the content"`: Không có quyền truy cập resource này

**Validation:**
- `"Client error: Incorrect passed data"`: Dữ liệu không hợp lệ
- `"Password must contain non-numeric characters"`: Mật khẩu phải chứa ký tự không phải số

---

## 🔄 Authentication Flow

### 1. Login lần đầu (Firebase)

```
FE (App)
  ↓
Lấy Firebase ID Token từ Firebase Auth SDK
  ↓
POST /api/auth/user-entity/login-firebase
Body: { "firebase_id_token": "..." }
  ↓
BE verify với Firebase (1 LẦN DUY NHẤT)
  ↓
BE tạo/tìm UserEntity
  ↓
BE tạo Access Token (JWT) - 7 ngày
BE tạo Refresh Token (JWT) - 30 ngày
  ↓
Response: { access_token, refresh_token, user }
  ↓
FE lưu tokens vào SharedPreferences
```

### 2. Các request tiếp theo

```
FE gửi request với Access Token
  ↓
Header: Authorization: Bearer <access_token>
  ↓
BE verify Access Token (JWT của BE) - NHANH
  ↓
BE lấy user_id từ token
  ↓
Xử lý logic (tự động filter theo user_id)
  ↓
Trả về response
```

### 3. Khi Access Token hết hạn

```
FE nhận lỗi 401 Unauthorized
  ↓
POST /api/auth/user-entity/refresh-token
Body: { "refresh_token": "..." }
  ↓
BE verify Refresh Token
  ↓
BE tạo Access Token mới (7 ngày)
BE tạo Refresh Token mới (30 ngày) - rotate
  ↓
Response: { access_token, refresh_token, user }
  ↓
FE lưu tokens mới vào SharedPreferences
```

---

## 📝 Notes

1. **Tự động filter theo user_id**: Tất cả các API (Task, Session, Goal, Setting) tự động filter data theo `user_id` của user đang đăng nhập. Không cần truyền `user_id` trong request.

2. **Tự động tạo user**: Khi login với Firebase, nếu user chưa tồn tại, hệ thống sẽ tự động tạo user mới.

3. **Tự động link Facebook**: Khi login với Facebook qua Firebase, hệ thống sẽ tự động tạo ExternalAccount để link Facebook.

4. **Token expiration**:
   - Access Token: 7 ngày
   - Refresh Token: 30 ngày

5. **Token rotation**: Mỗi lần refresh token, cả Access Token và Refresh Token đều được tạo mới.

---

## 🔗 Swagger Documentation

Bạn có thể xem và test API trực tiếp tại:
- Swagger UI: `http://localhost:8669/docs`
- ReDoc: `http://localhost:8669/re-docs`
- OpenAPI JSON: `http://localhost:8669/api/openapi.json`


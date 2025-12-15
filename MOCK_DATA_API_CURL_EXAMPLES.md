# Mock Data API - cURL Examples

## Base URL
```
http://localhost:8669/api/v1/mock-data
```

## Authentication
Tất cả các endpoints yêu cầu JWT token trong header:
```
Authorization: Bearer <your_access_token>
```

---

## 1. Tạo Fake Data cho Shop

**POST** `/api/v1/mock-data/shop?count=10`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/shop?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 10 sản phẩm shop",
    "count": 10,
    "items": [
      {
        "shop_id": 1,
        "name": "Synergistic scalable system engine",
        "price": 45.67,
        "type": "theme"
      },
      {
        "shop_id": 2,
        "name": "User-centric mission-critical leverage",
        "price": 23.45,
        "type": "avatar"
      }
    ]
  }
}
```

**Query Parameters:**
- `count` (optional): Số lượng sản phẩm cần tạo (1-100, mặc định: 10)

---

## 2. Tạo Fake Data cho Shop Purchases

**POST** `/api/v1/mock-data/shop-purchases?count=5`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/shop-purchases?count=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 5 purchase cho user 123",
    "count": 5,
    "purchases": [
      {
        "purchase_id": 1,
        "shop_id": 1,
        "shop_name": "Premium Theme",
        "purchased_at": 1703123600.456
      }
    ]
  }
}
```

**Lưu ý:** 
- Chỉ tạo purchase cho user hiện tại (từ JWT token)
- Cần có sản phẩm trong shop trước khi tạo purchase
- Không tạo purchase cho sản phẩm đã mua rồi

**Query Parameters:**
- `count` (optional): Số lượng purchase cần tạo (1-50, mặc định: 5)

---

## 3. Tạo Fake Data cho Tasks

**POST** `/api/v1/mock-data/tasks?count=10`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/tasks?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 10 task cho user 123",
    "count": 10,
    "tasks": [
      {
        "task_id": 1,
        "title": "Build scalable system architecture",
        "priority": "HIGH",
        "is_completed": 1
      },
      {
        "task_id": 2,
        "title": "Implement user authentication",
        "priority": "MEDIUM",
        "is_completed": 0
      }
    ]
  }
}
```

**Query Parameters:**
- `count` (optional): Số lượng task cần tạo (1-100, mặc định: 10)

**Fake Data Details:**
- Task date: Random trong 30 ngày qua hoặc 7 ngày tới
- Priority: HIGH, MEDIUM, hoặc LOW
- Một số task sẽ được đánh dấu là completed với completed_at

---

## 4. Tạo Fake Data cho Sessions

**POST** `/api/v1/mock-data/sessions?count=10`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/sessions?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 10 session cho user 123",
    "count": 10,
    "sessions": [
      {
        "session_id": 1,
        "session_type": "FOCUS_SESSION",
        "duration_minutes": 25,
        "status": "COMPLETED"
      },
      {
        "session_id": 2,
        "session_type": "SHORT_BREAK",
        "duration_minutes": 5,
        "status": "CANCELLED"
      }
    ]
  }
}
```

**Query Parameters:**
- `count` (optional): Số lượng session cần tạo (1-100, mặc định: 10)

**Fake Data Details:**
- Session date: Random trong 30 ngày qua
- Session type: FOCUS_SESSION (25 phút), SHORT_BREAK (5 phút), LONG_BREAK (15 phút)
- Status: COMPLETED hoặc CANCELLED

---

## 5. Tạo Fake Data cho Goals

**POST** `/api/v1/mock-data/goals?count=10`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/goals?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 10 goal cho user 123",
    "count": 10,
    "goals": [
      {
        "goal_id": 1,
        "goal_date": 1703123456.789,
        "target_sessions": 5,
        "completed_sessions": 5,
        "is_achieved": 1
      },
      {
        "goal_id": 2,
        "goal_date": 1703123500.123,
        "target_sessions": 8,
        "completed_sessions": 3,
        "is_achieved": 0
      }
    ]
  }
}
```

**Query Parameters:**
- `count` (optional): Số lượng goal cần tạo (1-100, mặc định: 10)

**Fake Data Details:**
- Goal date: Random trong 30 ngày qua
- Target sessions: 3-10 sessions
- Completed sessions: 0 đến target_sessions
- Completion percentage: Tự động tính
- is_achieved: 1 nếu completed >= target, 0 nếu không

---

## 6. Tạo Fake Data cho Users

**POST** `/api/v1/mock-data/users?count=5`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/users?count=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo 5 user",
    "count": 5,
    "users": [
      {
        "user_id": 124,
        "email": "john.doe@example.com",
        "display_name": "John Doe",
        "has_password": true
      },
      {
        "user_id": 125,
        "email": "jane.smith@example.com",
        "display_name": "Jane Smith",
        "has_password": false
      }
    ]
  }
}
```

**Query Parameters:**
- `count` (optional): Số lượng user cần tạo (1-50, mặc định: 5)

**Fake Data Details:**
- Email: Unique email từ Faker
- Display name: Random name
- Password: Một số user có password ("password123"), một số không (Firebase users)
- Profile picture: Random URL hoặc null
- Last login: Random trong 7 ngày qua

---

## 7. Tạo Fake Data cho Tất Cả Bảng

**POST** `/api/v1/mock-data/all?shop_count=10&tasks_count=10&sessions_count=10&goals_count=10&purchases_count=5`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/all?shop_count=10&tasks_count=10&sessions_count=10&goals_count=10&purchases_count=5' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Đã tạo fake data cho tất cả các bảng",
    "results": {
      "shop": {
        "message": "Đã tạo 10 sản phẩm shop",
        "count": 10,
        "items": [...]
      },
      "shop_purchases": {
        "message": "Đã tạo 5 purchase cho user 123",
        "count": 5,
        "purchases": [...]
      },
      "tasks": {
        "message": "Đã tạo 10 task cho user 123",
        "count": 10,
        "tasks": [...]
      },
      "sessions": {
        "message": "Đã tạo 10 session cho user 123",
        "count": 10,
        "sessions": [...]
      },
      "goals": {
        "message": "Đã tạo 10 goal cho user 123",
        "count": 10,
        "goals": [...]
      }
    }
  }
}
```

**Query Parameters:**
- `shop_count` (optional): Số lượng shop items (1-100, mặc định: 10)
- `tasks_count` (optional): Số lượng tasks (1-100, mặc định: 10)
- `sessions_count` (optional): Số lượng sessions (1-100, mặc định: 10)
- `goals_count` (optional): Số lượng goals (1-100, mặc định: 10)
- `purchases_count` (optional): Số lượng purchases (1-50, mặc định: 5)

---

## Ví dụ sử dụng thực tế

### 1. Tạo dữ liệu mẫu đầy đủ cho testing

```bash
# Bước 1: Tạo shop items
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/shop?count=20' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'

# Bước 2: Tạo purchases cho user hiện tại
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/shop-purchases?count=8' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'

# Bước 3: Tạo tasks
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/tasks?count=15' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'

# Bước 4: Tạo sessions
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/sessions?count=20' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'

# Bước 5: Tạo goals
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/goals?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 2. Tạo tất cả cùng lúc

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/all?shop_count=20&tasks_count=15&sessions_count=20&goals_count=10&purchases_count=8' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 3. Tạo nhiều users để test

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/mock-data/users?count=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

---

## Lưu ý

1. **Authentication**: Tất cả endpoints yêu cầu JWT token hợp lệ
2. **User-specific data**: Tasks, Sessions, Goals, và Shop Purchases được tạo cho user hiện tại (từ JWT token)
3. **Shop items**: Không chia theo user, tất cả user thấy cùng danh sách
4. **Unique constraints**: 
   - Email của users phải unique (Faker sẽ tự động tạo unique)
   - Shop purchases có unique constraint (user_id, shop_id)
5. **Dependencies**: 
   - Shop purchases cần có shop items trước
   - Nếu không có shop items, API sẽ trả về lỗi
6. **Rollback**: Nếu có lỗi, tất cả thay đổi sẽ được rollback
7. **Limits**: Mỗi endpoint có giới hạn số lượng tối đa để tránh quá tải

---

## Error Responses

### Không có shop items khi tạo purchases:
```json
{
  "http_code": 400,
  "success": false,
  "message": "Không có sản phẩm nào trong shop. Vui lòng tạo sản phẩm trước.",
  "metadata": null
}
```

### Email đã tồn tại (khi tạo users):
```json
{
  "http_code": 400,
  "success": false,
  "message": "Email đã tồn tại",
  "metadata": null
}
```


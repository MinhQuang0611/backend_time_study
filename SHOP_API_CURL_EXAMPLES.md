# Shop API - cURL Examples

## Base URL
```
http://localhost:8669/api/v1/shop
```

## Authentication
Tất cả các endpoints yêu cầu JWT token trong header:
```
Authorization: Bearer <your_access_token>
```

---

## 1. Tạo Sản Phẩm Mới (Admin)

**POST** `/api/v1/shop`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Premium Theme",
  "price": 9.99,
  "type": "theme"
}'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "shop_id": 1,
    "name": "Premium Theme",
    "price": 9.99,
    "type": "theme",
    "created_at": 1703123456.789,
    "updated_at": 1703123456.789
  }
}
```

---

## 2. Lấy Tất Cả Sản Phẩm (Với Trạng Thái Mua)

**GET** `/api/v1/shop?page=1&page_size=10&sort_by=price&sort_order=asc`

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop?page=1&page_size=10&sort_by=price&sort_order=asc' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": {
    "total": 10,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  },
  "data": [
    {
      "shop_id": 1,
      "name": "Premium Theme",
      "price": 9.99,
      "type": "theme",
      "is_purchased": false,
      "purchased_at": null,
      "created_at": 1703123456.789,
      "updated_at": 1703123456.789
    },
    {
      "shop_id": 2,
      "name": "Golden Avatar",
      "price": 7.99,
      "type": "avatar",
      "is_purchased": true,
      "purchased_at": 1703123500.123,
      "created_at": 1703123500.123,
      "updated_at": 1703123500.123
    }
  ]
}
```

---

## 3. Lấy Danh Sách Đã Mua

**GET** `/api/v1/shop/purchased?page=1&page_size=10`

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/purchased?page=1&page_size=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": {
    "total": 3,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  },
  "data": [
    {
      "shop_id": 2,
      "name": "Golden Avatar",
      "price": 7.99,
      "type": "avatar",
      "is_purchased": true,
      "purchased_at": 1703123500.123,
      "created_at": 1703123500.123,
      "updated_at": 1703123500.123
    }
  ]
}
```

---

## 4. Lấy Danh Sách Chưa Mua

**GET** `/api/v1/shop/not-purchased?page=1&page_size=10`

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/not-purchased?page=1&page_size=10' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": {
    "total": 7,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  },
  "data": [
    {
      "shop_id": 1,
      "name": "Premium Theme",
      "price": 9.99,
      "type": "theme",
      "is_purchased": false,
      "purchased_at": null,
      "created_at": 1703123456.789,
      "updated_at": 1703123456.789
    }
  ]
}
```

---

## 5. Lấy Thông Tin Sản Phẩm Theo ID (Với Trạng Thái Mua)

**GET** `/api/v1/shop/{shop_id}`

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "shop_id": 1,
    "name": "Premium Theme",
    "price": 9.99,
    "type": "theme",
    "is_purchased": false,
    "purchased_at": null,
    "created_at": 1703123456.789,
    "updated_at": 1703123456.789
  }
}
```

---

## 6. Kiểm Tra Trạng Thái Mua

**GET** `/api/v1/shop/{shop_id}/status`

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/1/status' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "shop_id": 1,
    "is_purchased": false,
    "purchased_at": null
  }
}
```

**Nếu đã mua:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "shop_id": 1,
    "is_purchased": true,
    "purchased_at": 1703123500.123
  }
}
```

---

## 7. Mua Sản Phẩm

**POST** `/api/v1/shop/{shop_id}/purchase`

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop/1/purchase' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Response:**
```json
{
  "http_code": 201,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "purchase_id": 1,
    "user_id": 123,
    "shop_id": 1,
    "purchased_at": 1703123600.456,
    "created_at": 1703123600.456,
    "updated_at": 1703123600.456
  }
}
```

**Lỗi nếu đã mua rồi:**
```json
{
  "http_code": 400,
  "success": false,
  "message": "Sản phẩm này đã được mua rồi",
  "metadata": null
}
```

---

## 8. Cập Nhật Sản Phẩm (Admin)

**PUT** `/api/v1/shop/{shop_id}`

```bash
curl -X 'PUT' \
  'http://localhost:8669/api/v1/shop/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Premium Theme Pro",
  "price": 14.99,
  "type": "theme"
}'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "shop_id": 1,
    "name": "Premium Theme Pro",
    "price": 14.99,
    "type": "theme",
    "created_at": 1703123456.789,
    "updated_at": 1703123800.123
  }
}
```

---

## 9. Xóa Sản Phẩm (Admin)

**DELETE** `/api/v1/shop/{shop_id}`

```bash
curl -X 'DELETE' \
  'http://localhost:8669/api/v1/shop/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

**Response:**
```json
{
  "http_code": 200,
  "success": true,
  "message": null,
  "metadata": null,
  "data": {
    "message": "Shop item deleted successfully"
  }
}
```

---

## Ví dụ sử dụng thực tế

### 1. Tạo nhiều sản phẩm

```bash
# Theme 1
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Dark Theme",
  "price": 5.99,
  "type": "theme"
}'

# Avatar 1
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Golden Avatar",
  "price": 7.99,
  "type": "avatar"
}'

# Pack 1
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Starter Pack",
  "price": 3.99,
  "type": "pack"
}'
```

### 2. User xem tất cả sản phẩm chưa mua

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/not-purchased?sort_by=price&sort_order=asc' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 3. User mua sản phẩm

```bash
curl -X 'POST' \
  'http://localhost:8669/api/v1/shop/1/purchase' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### 4. User xem danh sách đã mua

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/purchased' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

### 5. Kiểm tra trạng thái mua của một sản phẩm

```bash
curl -X 'GET' \
  'http://localhost:8669/api/v1/shop/1/status' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```

---

## Lưu ý

1. **Authentication**: Tất cả endpoints yêu cầu JWT token hợp lệ
2. **Shop không chia theo user**: Tất cả user thấy cùng danh sách sản phẩm
3. **Purchase status**: Mỗi user có trạng thái mua riêng cho từng sản phẩm
4. **type**: Có thể là bất kỳ string nào (ví dụ: "theme", "avatar", "pack", "item", v.v.)
5. **price**: Số thực (float), có thể có số thập phân
6. **is_purchased**: Boolean, `true` nếu user đã mua, `false` nếu chưa mua
7. **purchased_at**: Timestamp khi user mua sản phẩm (null nếu chưa mua)
8. **Error Responses**: 
   - Nếu mua lại sản phẩm đã mua: `400 Bad Request` với message "Sản phẩm này đã được mua rồi"
   - Nếu sản phẩm không tồn tại: `404 Not Found`

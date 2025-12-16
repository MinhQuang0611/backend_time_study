# Hướng dẫn Setup Firebase Credentials

## Bước 1: Đặt file Firebase credentials vào thư mục backend

1. Đổi tên file JSON bạn vừa tải từ Firebase Console thành: `firebase-credentials.json`
2. Đặt file vào thư mục `backend/` (cùng cấp với `docker-compose.yml`)

Cấu trúc thư mục sẽ như sau:
```
backend/
├── app/
├── alembic/
├── docker-compose.yml
├── .env
├── firebase-credentials.json  ← File này
└── ...
```

## Bước 2: Cập nhật file .env

Mở file `.env` và thêm các dòng sau:

```env
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

**Lưu ý:** 
- Thay `your-firebase-project-id` bằng Project ID thực tế của bạn
- Project ID có thể tìm thấy trong Firebase Console → Project Settings → General

## Bước 3: Restart Docker container

```bash
docker-compose down
docker-compose up --build
```

Hoặc nếu container đang chạy:

```bash
docker-compose restart app
```

## Bước 4: Kiểm tra logs

Sau khi restart, kiểm tra logs để xác nhận Firebase đã được khởi tạo:

```bash
docker-compose logs app | grep FIREBASE
```

Bạn sẽ thấy:
```
========== FIREBASE INITIALIZED WITH CREDENTIALS FILE: /app/firebase-credentials.json ==========
Project ID: your-project-id
```

## Bước 5: Test API

Thử gọi API login Firebase:

```bash
curl -X 'POST' \
  'http://localhost:8669/api/auth/user-entity/login-firebase' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "firebase_id_token": "YOUR_FIREBASE_ID_TOKEN"
}'
```

## ⚠️ Lưu ý bảo mật

1. **KHÔNG commit** file `firebase-credentials.json` lên Git
   - File đã được thêm vào `.gitignore`
   - Kiểm tra lại bằng: `git status` (file không nên xuất hiện)

2. **Bảo vệ file credentials:**
   - Chỉ người có quyền truy cập server mới được xem file này
   - Trong production, nên dùng secret management service

3. **Nếu file bị lộ:**
   - Vào Firebase Console → Project Settings → Service Accounts
   - Xóa service account key cũ
   - Tạo key mới

## Troubleshooting

### Lỗi: "File not found"
- Kiểm tra file `firebase-credentials.json` có tồn tại trong thư mục `backend/` không
- Kiểm tra đường dẫn trong `.env` có đúng không
- Kiểm tra file có được mount vào container không: `docker-compose exec app ls -la /app/firebase-credentials.json`

### Lỗi: "Invalid credentials"
- Kiểm tra file JSON có đúng format không
- Đảm bảo file là service account key từ Firebase Console
- Thử tải lại file từ Firebase Console

### Lỗi: "Project ID mismatch"
- Kiểm tra `FIREBASE_PROJECT_ID` trong `.env` có khớp với project ID trong file credentials không


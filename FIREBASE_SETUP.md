# Hướng dẫn cấu hình Firebase Authentication

## Vấn đề
Firebase Admin SDK cần **Service Account Credentials** để verify Firebase ID Tokens từ client.

## Cách 1: Sử dụng Service Account Key File (Khuyến nghị)

### Bước 1: Tải Service Account Key từ Firebase Console

1. Đăng nhập vào [Firebase Console](https://console.firebase.google.com/)
2. Chọn project của bạn
3. Vào **Project Settings** (biểu tượng bánh răng) → **Service Accounts**
4. Click **Generate new private key**
5. File JSON sẽ được tải xuống (ví dụ: `your-project-firebase-adminsdk-xxxxx.json`)

### Bước 2: Đặt file vào thư mục backend

1. Copy file JSON vừa tải vào thư mục `backend/`
2. Đổi tên file thành `firebase-credentials.json` (hoặc tên khác bạn muốn)

### Bước 3: Cấu hình trong `.env`

Thêm vào file `.env`:

```env
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
```

**Lưu ý:** 
- Thay `your-firebase-project-id` bằng Project ID thực tế của bạn (có thể tìm thấy trong Firebase Console → Project Settings → General)
- Đường dẫn `FIREBASE_CREDENTIALS_PATH` có thể là đường dẫn tuyệt đối hoặc tương đối từ thư mục backend

### Bước 4: Restart Docker container

```bash
docker-compose restart app
```

## Cách 2: Sử dụng GOOGLE_APPLICATION_CREDENTIALS

Nếu bạn đã có file credentials và muốn dùng environment variable:

1. Đặt file credentials vào thư mục backend
2. Thêm vào `.env`:

```env
FIREBASE_PROJECT_ID=your-firebase-project-id
GOOGLE_APPLICATION_CREDENTIALS=/app/firebase-credentials.json
```

**Lưu ý:** Đường dẫn trong Docker container là `/app/` (không phải `./`)

## Cách 3: Application Default Credentials (ADC)

Chỉ hoạt động khi:
- Chạy trên Google Cloud Platform (GCP)
- Hoặc đã setup Application Default Credentials trên máy local

Chỉ cần set:

```env
FIREBASE_PROJECT_ID=your-firebase-project-id
```

## Kiểm tra cấu hình

Sau khi restart container, kiểm tra logs:

```bash
docker-compose logs app | grep FIREBASE
```

Bạn sẽ thấy:
- `========== FIREBASE INITIALIZED WITH CREDENTIALS FILE: ... ==========`
- `Project ID: your-project-id`

Nếu thấy lỗi, kiểm tra:
1. File credentials có tồn tại không
2. Đường dẫn trong `.env` có đúng không
3. File credentials có đúng format JSON không

## Bảo mật

⚠️ **QUAN TRỌNG:**
- **KHÔNG** commit file `firebase-credentials.json` vào Git
- Thêm vào `.gitignore`:
  ```
  firebase-credentials.json
  *.json
  ```
- File credentials chứa private key, cần được bảo mật cẩn thận

## Troubleshooting

### Lỗi: "DefaultCredentialsError"
- **Nguyên nhân:** Không tìm thấy credentials
- **Giải pháp:** Sử dụng Cách 1 hoặc Cách 2 ở trên

### Lỗi: "A project ID is required"
- **Nguyên nhân:** `FIREBASE_PROJECT_ID` chưa được set
- **Giải pháp:** Thêm `FIREBASE_PROJECT_ID` vào `.env`

### Lỗi: "File not found"
- **Nguyên nhân:** Đường dẫn credentials file không đúng
- **Giải pháp:** Kiểm tra lại đường dẫn trong `.env`, đảm bảo file tồn tại


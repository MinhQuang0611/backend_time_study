# Hướng dẫn tạo Migration cho Shop Table

## Bước 1: Tạo migration file

Chạy lệnh sau để tạo migration file tự động:

```bash
alembic revision --autogenerate --rev-id add_shop_table
```

Hoặc nếu đang chạy trong Docker:

```bash
docker-compose exec app alembic revision --autogenerate --rev-id add_shop_table
```

## Bước 2: Kiểm tra migration file

File migration sẽ được tạo trong `alembic/versions/` với tên như:
- `xxxxx_add_shop_table.py`

Mở file và kiểm tra xem có đúng các trường:
- `shop_id` (Integer, primary key, autoincrement)
- `name` (String, nullable=False)
- `price` (Float, nullable=False)
- `is_purchased` (Integer, default=0)
- `type` (String, nullable=True)
- `created_at` (Float)
- `updated_at` (Float)

## Bước 3: Apply migration

Chạy lệnh để apply migration:

```bash
alembic upgrade head
```

Hoặc trong Docker:

```bash
docker-compose exec app alembic upgrade head
```

## Bước 4: Kiểm tra table đã được tạo

Kiểm tra trong database hoặc qua API:

```bash
# Kiểm tra table đã tồn tại
docker-compose exec db psql -U postgres -d your_database -c "\d shop"
```

## Lưu ý

- Nếu migration file không tự động detect model mới, kiểm tra:
  1. Model `ShopEntity` đã được import trong `app/models/__init__.py`
  2. File migration có import đúng model không
  3. Có thể cần chỉnh sửa thủ công migration file

- Nếu có lỗi khi apply migration, có thể rollback:
  ```bash
  alembic downgrade -1
  ```


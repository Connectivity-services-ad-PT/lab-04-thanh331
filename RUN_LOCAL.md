# Hướng dẫn khởi chạy nhanh dịch vụ Analytics Service (Nhóm B5)

Tài liệu hướng dẫn triển khai và kiểm thử ứng dụng đóng gói trong Docker Container cho hệ thống Smart Campus.

## Các bước triển khai nhanh trong 3 bước:

### Bước 1: Chuẩn bị cấu hình môi trường dữ liệu
Sao chép cấu hình mẫu runtime để container nhận diện tham số bảo mật:
```powershell
cp .env.example .env
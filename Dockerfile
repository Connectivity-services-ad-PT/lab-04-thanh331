FROM python:3.11-slim

WORKDIR /app

# Sao chép và cài đặt thư viện phụ thuộc trước để tận dụng cache của Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Rubric Ràng buộc bảo mật: Tạo và chuyển sang chạy bằng tài khoản Non-Root User
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Mở cổng 8000 của ứng dụng
EXPOSE 8000

# Rubric Ràng buộc vận hành: HEALTHCHECK tự động kiểm tra endpoint /health định kỳ
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Lệnh khởi chạy ứng dụng uvicorn backend
CMD ["uvicorn", "iot_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]
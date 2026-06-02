from fastapi import FastAPI, Response, Header, Query, status
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid

app = FastAPI(title="B5 - Analytics Service API")

# Cấu hình Token cứng để test bảo mật
VALID_TOKEN = "local-dev-token-analytics-xyz"

def get_problem_details(title: str, status_code: int, detail: str, instance: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "type": f"https://api.smartcampus.edu.vn/errors/{status_code}",
            "title": title,
            "status": status_code,
            "detail": detail,
            "instance": f"https://api.smartcampus.edu.vn{instance}"
        },
        headers={"Content-Type": "application/problem+json"}
    )

@app.get("/health")
def check_health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/api/v1/analytics/summary")
def get_dashboard_summary(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return get_problem_details("Unauthorized", 401, "Lỗi xác thực do thiếu hoặc sai định dạng Token", "/api/v1/analytics/summary")
    
    token = authorization.split(" ")[1]
    if token != VALID_TOKEN:
        return get_problem_details("Unauthorized", 401, "Token không hợp lệ hoặc đã hết hạn", "/api/v1/analytics/summary")

    return {
        "total_records": 12540,
        "system_efficiency": 94.5,
        "last_updated_by": "b5_processor"
    }

@app.post("/api/v1/analytics/reports", status_code=201)
def create_analytics_report(payload: dict):
    # Kiểm tra thiếu trường dữ liệu biên để giả lập lỗi 400 Bad Request
    if not payload or "start_date" not in payload or "end_date" not in payload:
        return get_problem_details("Invalid Input Parameters", 400, "Tham số đầu vào thiếu trường bắt buộc.", "/api/v1/analytics/reports")
    
    return {
        "report_id": str(uuid.uuid4()),
        "status": "pending"
    }

@app.get("/api/v1/analytics/anomalies")
def get_anomaly_events(page: int = Query(1), limit: int = Query(10)):
    if page < 1 or limit < 1 or limit > 100:
        return get_problem_details("Invalid Pagination", 400, "Tham số phân trang truyền vào không hợp lệ", "/api/v1/analytics/anomalies")
        
    return [
        {
            "event_id": str(uuid.uuid4()),
            "type": "IoTAnomaly",
            "detected_at": datetime.utcnow().isoformat() + "Z",
            "sensor_id": "SENSOR-102",
            "threshold_exceeded": 45.2
        }
    ]
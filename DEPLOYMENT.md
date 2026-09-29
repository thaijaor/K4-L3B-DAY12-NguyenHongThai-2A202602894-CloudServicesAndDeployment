# Thông Tin Deploy — Checkpoint 5

> Chỉ ghi tên biến môi trường, tuyệt đối không ghi giá trị API key.

## Thông Tin Học Viên

| Mục | Nội dung |
|-----|----------|
| Họ và tên | Nguyễn Hồng Thái |
| Mã học viên | 2A202602894 |
| Repo | https://github.com/thaijaor/K4-L3B-DAY12-NguyenHongThai-2A202602894-CloudServicesAndDeployment |

## Service

| Mục | Nội dung |
|-----|----------|
| Public URL | https://agent-production-5750.up.railway.app |
| Platform | Railway |
| Project | K4-L3B-D12-CloudDeploy |
| Environment | production |
| Ngày deploy | 2026-09-29 |

## Biến Môi Trường Đã Set Trên Cloud

| Biến | Đã set | Nguồn |
|------|--------|-------|
| `PORT` | Có | Railway tự gán |
| `AGENT_API_KEY` | Có | Railway service variable; giá trị nằm trong `.env` local bị gitignore |
| `REDIS_URL` | Có | `redis://redis.railway.internal:6379/0`, Redis service cùng project |
| `RATE_LIMIT_PER_MINUTE` | Có | `10` |
| `MONTHLY_BUDGET_USD` | Có | `10.0` |
| `LOG_LEVEL` | Có | `INFO` |

## Kết Quả Chạy Thật

```text
GET /health                         200  {"status":"ok","service":"day12-agent","version":"1.0.0"}
GET /ready                          200  {"status":"ready","redis":true}
POST /ask không có API key          401
POST /ask có API key                200
POST /ask lần 1, cùng X-User-Id     history_length=0
POST /ask lần 2, cùng X-User-Id     history_length=2
```

Railway build và chạy image thành công; Redis service cũng ở trạng thái `SUCCESS`.

## Ảnh Minh Chứng CP5

Ảnh Railway production ngày 2026-09-29: deployment `64e24d34` đang Active, Redis Online; log ghi nhận `/health` và `/ready` trả `200`, `/ask` thiếu API key trả `401`, và `/docs` cùng `/openapi.json` trả `200`.

![Railway deployment và runtime logs](screenshots/cp5-railway-deployment-logs.png)

## Kiểm Tra Thủ Công

```bash
curl -i https://agent-production-5750.up.railway.app/health
curl -i https://agent-production-5750.up.railway.app/ready
curl -i -X POST https://agent-production-5750.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello"}'
```

Request `/ask` hợp lệ cần thêm hai header `X-API-Key` và `X-User-Id`. Không đưa giá trị key vào lệnh được commit hoặc tài liệu công khai.

## CI/CD Trên GitHub Actions

Workflow `.github/workflows/ci.yml` chạy test và build Docker khi push hoặc mở pull request. Railway GitHub App được cài cho repo; service `Agent` theo dõi nhánh `main`, với Auto Deploy và Wait for CI bật trong dashboard. Run #4 trên commit `7c64867` đã xanh, nhưng deployment Railway bắt đầu lúc `04:40:11Z`, trước khi Actions bắt đầu lúc `04:40:12Z` và hoàn tất lúc `04:40:55Z`. Vì vậy Auto Deploy hoạt động, còn CI gate chưa chặn deployment dù toggle đang bật.

Đây là cách deploy đang dùng, không cần GitHub Actions secret hay repository variable. Deployment `ab8b63ef-0505-4a7d-a890-8436acb264f4` thành công; `/health` trả `200` và `/ready` trả `200` với Redis sẵn sàng.

Workflow giữ một job **Optional Railway CLI deploy** cho phương án deploy trực tiếp từ GitHub Actions. Job này chỉ chạy khi khai báo đủ các biến bên dưới; hiện tại nó được bỏ qua để tránh chạy song song với Railway Auto Deploy. Không bật cả hai cách cùng lúc.

Nếu chủ động chọn phương án Railway CLI, thêm secret `RAILWAY_TOKEN` (project token) và các repository variables sau:

| Repository variable | Giá trị |
|---------------------|---------|
| `RAILWAY_PROJECT_ID` | `ec1dfd07-0f1a-4f90-9c57-ca77b2a8474b` |
| `RAILWAY_ENVIRONMENT_ID` | `2210a3ad-cee6-4c0b-8dde-21a01ea3f2a8` |
| `RAILWAY_SERVICE_ID` | `cf6f4935-e7a1-4eb5-881d-425555db4d85` |
| `PUBLIC_URL` | `https://agent-production-5750.up.railway.app` |

Không commit Railway token hoặc giá trị API key.

---

## Nếu Dùng Phương Án Dự Phòng

Không áp dụng. Service đã deploy trên Railway và các endpoint `/health`, `/ready`, `/ask` đã được kiểm tra trực tiếp.

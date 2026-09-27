# 新北市自行車即時資訊系統

全端應用,展示新北市 YouBike 站點即時資訊,支援會員登入與收藏站點。

## 專案結構

```
bike_project/
  backend/    # FastAPI + PostgreSQL + Redis
  frontend/   # Vue3 + SCSS + TailwindCSS + daisyUI + Leaflet
```

## 本機啟動方式

### 前置需求
- PostgreSQL(本機已啟動服務,建立好 `bike_db` 資料庫與帳號)
- Redis(本機已啟動服務,預設 port 6379)
- Python 3.11+
- Node.js 20+

### 後端
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
cp .env.example .env            # 依本機 PostgreSQL/Redis 設定調整
alembic upgrade head
uvicorn app.main:app --reload
```
後端預設跑在 http://localhost:8000,API 文件在 http://localhost:8000/docs

### 前端
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
前端預設跑在 http://localhost:5173

## 資料來源
新北市政府資料開放平台 — YouBike2.0 即時資訊
https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json

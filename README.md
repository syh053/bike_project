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
- Python 3.11+ 與 [uv](https://docs.astral.sh/uv/)
- Node.js 20+ 與 [pnpm](https://pnpm.io/)

### 後端
```bash
cd backend
uv sync                         # 自動建立 .venv 並安裝 pyproject.toml/uv.lock 鎖定的套件
cp .env.example .env            # 依本機 PostgreSQL/Redis 設定調整
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```
後端預設跑在 http://localhost:8000,API 文件在 http://localhost:8000/docs

### 前端
```bash
cd frontend
pnpm install
cp .env.example .env
pnpm run dev
```
前端預設跑在 http://localhost:5173

## Docker 部署

不需要本機安裝 PostgreSQL/Redis/Node,直接用 Docker Compose 啟動整套服務:

```bash
docker compose up --build
```

- 前端:http://localhost:5173
- 後端 API:http://localhost:8000/api
- 後端 Swagger 文件:http://localhost:8000/docs

第一次啟動時後端會自動執行 `alembic upgrade head` 建立資料表,資料庫資料會保存在 named volume(`pgdata`),重啟容器不會遺失。

> 注意:前端的 `VITE_API_BASE_URL` 是編譯期(build-time)寫死進靜態檔案的,如果要更換後端對外的 host/port,需要重新 build 前端 image(`docker compose build frontend`)才會生效。
>
> `docker-compose.yml` 裡的資料庫帳密與 `backend/.env.docker.example` 裡的 `SECRET_KEY` 都只是開發用預設值,正式對外部署前請務必更換。

## 資料來源
新北市政府資料開放平台 — YouBike2.0 即時資訊
https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json

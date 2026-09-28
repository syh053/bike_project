# Backend - YouBike 即時資訊系統

FastAPI + PostgreSQL(SQLAlchemy + Alembic)+ Redis(redis.asyncio)。

## 環境需求

- Python 3.11+(專案以 `.python-version` 鎖定 3.11,與 Docker image 一致)
- [uv](https://docs.astral.sh/uv/) 套件管理工具
- PostgreSQL(本機需先建立資料庫與帳號,對應 `.env` 的 `DATABASE_URL`)
- Redis

## 安裝

```bash
uv sync                       # 自動建立 .venv 並安裝 pyproject.toml/uv.lock 鎖定的套件
copy .env.example .env        # 依實際環境調整內容
```

> 若開發機的防毒/資安軟體會攔截並重簽對外 HTTPS 連線(導致 `uv sync` 出現憑證驗證錯誤),
> `pyproject.toml` 的 `[tool.uv]` 已預設開啟 `native-tls = true`,讓 uv 改用系統信任庫(本機
> Windows 通常已經信任該憑證)。在 Docker 容器內則另外透過 `certs/` 資料夾 + `update-ca-certificates`
> 把同一張憑證匯入容器的系統信任庫(見 `Dockerfile`)。

## 環境變數說明(`.env`)

| 變數 | 說明 |
|---|---|
| `DATABASE_URL` | PostgreSQL 連線字串(SQLAlchemy + psycopg 格式) |
| `REDIS_URL` | Redis 連線字串 |
| `SESSION_COOKIE_NAME` | 登入 session 的 cookie 名稱 |
| `SESSION_TTL_SECONDS` | 登入 session 存活時間(秒),預設 7 天 |
| `STATION_CACHE_KEY` | 站點快取(fresh)在 Redis 的 key |
| `STATION_CACHE_TTL_SECONDS` | 站點快取(fresh)TTL,預設 45 秒 |
| `STATION_CACHE_STALE_TTL_SECONDS` | 站點快取(stale 備援)TTL,預設 300 秒 |
| `STATION_CACHE_LOCK_KEY` | single-flight 鎖的 key |
| `STATION_CACHE_LOCK_TTL_SECONDS` | 鎖的 TTL,避免抓取失敗時鎖住不放 |
| `NTPC_API_BASE_URL` | 新北市開放資料 YouBike2.0 API 位址 |
| `NTPC_API_PAGE_SIZE` | 每頁筆數(對應上游 API 的 page/size 參數) |
| `NTPC_API_MAX_PAGES` | 分頁防呆上限,避免上游異常時無窮迴圈 |
| `CORS_ORIGINS` | 允許的前端來源(逗號分隔) |
| `APP_ENV` | 環境標記(development/production 等) |
| `SECRET_KEY` | 保留欄位,正式環境請更換 |

## 建立資料庫 Schema

```bash
uv run alembic upgrade head
```

若需要新增 migration:

```bash
uv run alembic revision --autogenerate -m "訊息"
uv run alembic upgrade head
```

## 啟動

```bash
uv run uvicorn app.main:app --reload
```

啟動後可開啟 http://localhost:8000/docs 查看互動式 API 文件。

## 已知環境注意事項(Windows)

- **passlib 與新版 bcrypt 不相容**:`passlib==1.7.4` 呼叫 `bcrypt.__about__.__version__` 這個新版 `bcrypt`(5.x)已移除的屬性,雜湊密碼時會丟出 `password cannot be longer than 72 bytes` 之類的錯誤。本專案已在 `pyproject.toml` 鎖定 `bcrypt==4.0.1`,重建環境時請勿升級此套件版本,除非同時升級 passlib 並驗證相容性。
- **Windows 上 httpx 對新北市開放資料 API 的 SSL 驗證失敗**:純用 `certifi` 內建憑證鏈連線 `https://data.ntpc.gov.tw` 會出現 `CERTIFICATE_VERIFY_FAILED: unable to get local issuer certificate`,但 Windows 內建信任庫(curl 走的 schannel)可以正常驗證。因此 `app/services/ntpc_client.py` 改用 `truststore` 套件,讓 Python 的 SSL context 直接讀取作業系統信任庫,不再依賴 certifi。

## 快速自我測試(curl)

```bash
# 健康檢查
curl http://localhost:8000/api/health

# 註冊
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"displayName\":\"Test\"}"

# 登入(保存 cookie 到 cookies.txt)
curl -c cookies.txt -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"

# 取得目前登入者
curl -b cookies.txt http://localhost:8000/api/auth/me

# 登出
curl -b cookies.txt -X POST http://localhost:8000/api/auth/logout

# 站點列表
curl http://localhost:8000/api/stations

# 行政區列表
curl http://localhost:8000/api/stations/areas

# 收藏站點(需先登入,沿用上面的 cookies.txt)
curl -b cookies.txt -X POST http://localhost:8000/api/favorites \
  -H "Content-Type: application/json" \
  -d "{\"stationNo\":\"500201001\"}"

# 收藏列表
curl -b cookies.txt http://localhost:8000/api/favorites

# 取消收藏
curl -b cookies.txt -X DELETE http://localhost:8000/api/favorites/500201001
```

## 專案結構

```
app/
  main.py                 FastAPI app、CORS、router 掛載、統一 exception handler
  core/                   設定、資料庫、Redis、密碼/session 工具
  models/                 SQLAlchemy ORM models
  schemas/                Pydantic schemas(API request/response)
  api/                    路由與依賴注入(get_current_user)
  services/               業務邏輯(NTPC client、站點快取、auth、favorites)
  exceptions.py           統一例外處理
alembic/                  資料庫 migration
```

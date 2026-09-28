FROM python:3.11-slim

# truststore（app/services/ntpc_client.py）需要系統信任庫才能驗證 TLS
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 開發機防毒軟體對外部 HTTPS 連線做憑證掃描攔截時,uv/系統信任庫需額外信任其重簽憑證才能連上
# pypi.org 等外部服務;certs/ 內沒有對應憑證檔的環境(如 CI、其他開發機)則此步驟不影響任何東西
COPY certs/ /usr/local/share/ca-certificates/extra/
RUN update-ca-certificates

COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /usr/local/bin/

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["sh", "/app/docker-entrypoint.sh"]

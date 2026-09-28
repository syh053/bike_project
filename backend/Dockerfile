FROM python:3.11-slim

# truststore（app/services/ntpc_client.py）需要系統信任庫才能驗證 TLS
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 開發機防毒軟體對外部 HTTPS 連線做憑證掃描攔截時,pip/系統信任庫需額外信任其重簽憑證才能連上
# pypi.org 等外部服務;certs/ 內沒有對應憑證檔的環境(如 CI、其他開發機)則此步驟不影響任何東西
COPY certs/ /usr/local/share/ca-certificates/extra/
RUN update-ca-certificates
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "/app/docker-entrypoint.sh"]

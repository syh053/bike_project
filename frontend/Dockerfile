# Stage 1: build
FROM node:20-slim AS build
WORKDIR /app
# 開發機防毒軟體對外部 HTTPS 連線做憑證掃描攔截時,npm 需額外信任其重簽憑證才能連上 npm registry;
# certs/ 內沒有對應憑證檔的環境(如 CI、其他開發機)只會在 build log 印出可忽略的 warning
COPY certs/ ./certs/
ENV NODE_EXTRA_CA_CERTS=/app/certs/avg-root.crt
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_API_BASE_URL=http://localhost:8000/api
ARG VITE_MAP_DEFAULT_LAT=25.0170
ARG VITE_MAP_DEFAULT_LNG=121.4620
ARG VITE_MAP_DEFAULT_ZOOM=12
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL \
    VITE_MAP_DEFAULT_LAT=$VITE_MAP_DEFAULT_LAT \
    VITE_MAP_DEFAULT_LNG=$VITE_MAP_DEFAULT_LNG \
    VITE_MAP_DEFAULT_ZOOM=$VITE_MAP_DEFAULT_ZOOM
RUN npm run build

# Stage 2: serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

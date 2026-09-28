from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+psycopg://bikeuser:bikepass@localhost:5432/bike_db"
    redis_url: str = "redis://localhost:6379/0"

    session_cookie_name: str = "session_id"
    session_ttl_seconds: int = 604800

    station_cache_key: str = "ntpc:stations:all"
    station_cache_ttl_seconds: int = 45
    station_cache_stale_ttl_seconds: int = 300
    station_cache_lock_key: str = "ntpc:stations:lock"
    station_cache_lock_ttl_seconds: int = 10

    ntpc_api_base_url: str = "https://data.ntpc.gov.tw/api/datasets/010e5b15-3823-4b20-b401-b1cf000550c5/json"
    ntpc_api_page_size: int = 100
    ntpc_api_max_pages: int = 50

    cors_origins: str = "http://localhost:5173"
    app_env: str = "development"
    secret_key: str = "change-me-in-prod"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def station_cache_stale_key(self) -> str:
        return f"{self.station_cache_key}:stale"


settings = Settings()

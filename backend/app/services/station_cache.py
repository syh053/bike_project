import asyncio
import json
from datetime import datetime, timezone

from app.core.config import settings
from app.core.redis_client import redis_client
from app.services import ntpc_client

_COLD_START_RETRY_COUNT = 5
_COLD_START_RETRY_DELAY_SECONDS = 0.5


def _cache_age_seconds(fetched_at: str) -> int:
    fetched = datetime.fromisoformat(fetched_at)
    now = datetime.now(timezone.utc)
    return max(0, int((now - fetched).total_seconds()))


def _build_result(payload: dict, *, cached: bool, stale: bool) -> dict:
    return {
        "stations": payload["stations"],
        "cached": cached,
        "stale": stale,
        "cacheAgeSeconds": 0 if not cached else _cache_age_seconds(payload["fetchedAt"]),
        "updatedAt": payload["fetchedAt"],
    }


async def _fetch_and_cache() -> dict:
    stations = await ntpc_client.fetch_all_stations()
    payload = {
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "stations": stations,
    }
    raw = json.dumps(payload)
    await redis_client.set(settings.station_cache_key, raw, ex=settings.station_cache_ttl_seconds)
    await redis_client.set(settings.station_cache_stale_key, raw, ex=settings.station_cache_stale_ttl_seconds)
    return payload


async def _try_acquire_lock() -> bool:
    acquired = await redis_client.set(
        settings.station_cache_lock_key, "1", nx=True, ex=settings.station_cache_lock_ttl_seconds
    )
    return bool(acquired)


async def get_all() -> dict:
    raw = await redis_client.get(settings.station_cache_key)
    if raw:
        return _build_result(json.loads(raw), cached=True, stale=False)

    if await _try_acquire_lock():
        try:
            payload = await _fetch_and_cache()
        finally:
            await redis_client.delete(settings.station_cache_lock_key)
        return _build_result(payload, cached=False, stale=False)

    stale_raw = await redis_client.get(settings.station_cache_stale_key)
    if stale_raw:
        return _build_result(json.loads(stale_raw), cached=True, stale=True)

    # 冷啟動:沒有 fresh cache、沒有 stale 備援、也沒搶到鎖 -> 短暫重試，最後直接同步抓取
    for _ in range(_COLD_START_RETRY_COUNT):
        await asyncio.sleep(_COLD_START_RETRY_DELAY_SECONDS)

        raw = await redis_client.get(settings.station_cache_key)
        if raw:
            return _build_result(json.loads(raw), cached=True, stale=False)

        if await _try_acquire_lock():
            try:
                payload = await _fetch_and_cache()
            finally:
                await redis_client.delete(settings.station_cache_lock_key)
            return _build_result(payload, cached=False, stale=False)

    payload = await _fetch_and_cache()
    return _build_result(payload, cached=False, stale=False)

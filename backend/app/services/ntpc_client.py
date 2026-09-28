import ssl
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx
import truststore

from app.core.config import settings

_ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

TAIPEI_TZ = ZoneInfo("Asia/Taipei")


def _parse_mday(mday: str) -> str:
    dt = datetime.strptime(mday, "%Y%m%dT%H%M%S").replace(tzinfo=TAIPEI_TZ)
    return dt.isoformat()


def _normalize_station(raw: dict) -> dict:
    return {
        "sno": raw["sno"],
        "sna": raw["sna"],
        "snaen": raw.get("snaen"),
        "sarea": raw.get("sarea"),
        "sareaen": raw.get("sareaen"),
        "ar": raw.get("ar"),
        "aren": raw.get("aren"),
        "lat": float(raw["lat"]),
        "lng": float(raw["lng"]),
        "totalQuantity": int(raw["tot_quantity"]),
        "availableRent": int(raw["sbi_quantity"]),
        "availableReturn": int(raw["bemp"]),
        "yb2Quantity": int(raw["yb2_quantity"]),
        "eybQuantity": int(raw["eyb_quantity"]),
        "active": raw.get("act") == "1",
        "updateTime": _parse_mday(raw["mday"]),
    }


async def fetch_all_stations() -> list[dict]:
    stations: list[dict] = []
    page_size = settings.ntpc_api_page_size

    async with httpx.AsyncClient(timeout=10.0, verify=_ssl_context) as client:
        for page in range(settings.ntpc_api_max_pages):
            response = await client.get(
                settings.ntpc_api_base_url,
                params={"page": page, "size": page_size},
            )
            response.raise_for_status()
            page_data = response.json()

            if not page_data:
                break

            stations.extend(_normalize_station(raw) for raw in page_data)

            if len(page_data) < page_size:
                break

    return stations

from fastapi import APIRouter, HTTPException, status

from app.schemas.station import Station, StationAreasResponse, StationListResponse
from app.services import station_cache

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("", response_model=StationListResponse, response_model_by_alias=True)
async def list_stations(
    sarea: str | None = None,
    keyword: str | None = None,
    active_only: bool = False,
) -> StationListResponse:
    result = await station_cache.get_all()
    stations = result["stations"]
    total = len(stations)

    filtered = stations
    if sarea:
        filtered = [s for s in filtered if s.get("sarea") == sarea]
    if keyword:
        filtered = [s for s in filtered if keyword in (s.get("sna") or "")]
    if active_only:
        filtered = [s for s in filtered if s.get("active") is True]

    return StationListResponse(
        updatedAt=result["updatedAt"],
        cached=result["cached"],
        stale=result["stale"],
        cacheAgeSeconds=result["cacheAgeSeconds"],
        total=total,
        data=[Station(**s) for s in filtered],
    )


@router.get("/areas", response_model=StationAreasResponse)
async def list_areas() -> StationAreasResponse:
    result = await station_cache.get_all()
    areas = sorted({s["sarea"] for s in result["stations"] if s.get("sarea")})
    return StationAreasResponse(areas=areas)


@router.get("/{sno}", response_model=Station, response_model_by_alias=True)
async def get_station(sno: str) -> Station:
    result = await station_cache.get_all()
    for s in result["stations"]:
        if s["sno"] == sno:
            return Station(**s)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到此站點")

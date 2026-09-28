from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user
from app.core.db import get_db
from app.schemas.favorite import FavoriteCreateRequest, FavoriteCreateResponse, FavoriteResponse
from app.schemas.station import Station
from app.services import favorite_service, station_cache

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("", response_model=list[FavoriteResponse], response_model_by_alias=True)
async def list_favorites(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[FavoriteResponse]:
    favorites = favorite_service.list_favorites(db, user_id=current_user.id)

    result = await station_cache.get_all()
    stations_by_sno = {s["sno"]: s for s in result["stations"]}

    return [
        FavoriteResponse(
            stationNo=favorite.station_no,
            createdAt=favorite.created_at.isoformat(),
            station=Station(**stations_by_sno[favorite.station_no]) if favorite.station_no in stations_by_sno else None,
        )
        for favorite in favorites
    ]


@router.post("", response_model=FavoriteCreateResponse, status_code=status.HTTP_201_CREATED, response_model_by_alias=True)
async def create_favorite(
    payload: FavoriteCreateRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FavoriteCreateResponse:
    result = await station_cache.get_all()
    station = next((s for s in result["stations"] if s["sno"] == payload.station_no), None)
    if station is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到此站點")

    if favorite_service.get_favorite(db, user_id=current_user.id, station_no=payload.station_no) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="已收藏過此站點")

    favorite = favorite_service.create_favorite(
        db, user_id=current_user.id, station_no=payload.station_no, station_name=station["sna"]
    )
    return FavoriteCreateResponse(stationNo=favorite.station_no, createdAt=favorite.created_at.isoformat())


@router.delete("/{station_no}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(
    station_no: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    favorite = favorite_service.get_favorite(db, user_id=current_user.id, station_no=station_no)
    if favorite is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到收藏紀錄")

    favorite_service.delete_favorite(db, favorite=favorite)

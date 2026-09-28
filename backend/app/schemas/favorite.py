from pydantic import BaseModel, ConfigDict, Field

from app.schemas.station import Station


class FavoriteCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    station_no: str = Field(alias="stationNo")


class FavoriteCreateResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    station_no: str = Field(alias="stationNo")
    created_at: str = Field(alias="createdAt")


class FavoriteResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    station_no: str = Field(alias="stationNo")
    created_at: str = Field(alias="createdAt")
    station: Station | None = None

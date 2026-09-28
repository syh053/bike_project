from pydantic import BaseModel, ConfigDict, Field


class Station(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sno: str
    sna: str
    snaen: str | None = None
    sarea: str | None = None
    sareaen: str | None = None
    ar: str | None = None
    aren: str | None = None
    lat: float
    lng: float
    total_quantity: int = Field(alias="totalQuantity")
    available_rent: int = Field(alias="availableRent")
    available_return: int = Field(alias="availableReturn")
    yb2_quantity: int = Field(alias="yb2Quantity")
    eyb_quantity: int = Field(alias="eybQuantity")
    active: bool
    update_time: str = Field(alias="updateTime")


class StationListResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    updated_at: str = Field(alias="updatedAt")
    cached: bool
    stale: bool
    cache_age_seconds: int = Field(alias="cacheAgeSeconds")
    total: int
    data: list[Station]


class StationAreasResponse(BaseModel):
    areas: list[str]

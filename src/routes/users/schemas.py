from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
import uuid

from src.routes.devices.schemas import DeviceSchema, StatsValues


class PartialUserSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class FullUserSchema(PartialUserSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)


class UserWithDevicesSchema(FullUserSchema):
    devices: List[DeviceSchema] = []


class UserAggregatedStatsResponse(BaseModel):
    user_id: uuid.UUID
    total_devices: int
    total_measurements: int
    period: Dict[str, Optional[datetime]]
    stats: Dict[str, StatsValues]


class UserDeviceStatsResponse(BaseModel):
    user_id: uuid.UUID
    total_devices: int
    total_measurements: int
    period: Dict[str, Optional[datetime]]
    devices: List["DeviceStats"]


class DeviceStats(BaseModel):
    device_id: uuid.UUID
    stats: Dict[str, StatsValues]

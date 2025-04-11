from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, Field

class PartialDeviceSchema(BaseModel):
    """Base schema for device creation."""
    serial_number: str = Field(..., min_length=3, max_length=30)


class DeviceSchema(PartialDeviceSchema):
    """Complete device representation including system-generated ID.

    Extends PartialDeviceSchema with:
        id: Universally unique identifier for the device.
    """
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class MeasurementCreateSchema(BaseModel):
    x: float
    y: float
    z: float

class MeasurementSchema(MeasurementCreateSchema):
    id: uuid.UUID
    device_id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True

class StatsValues(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float

class DeviceStatsResponse(BaseModel):
    device_id: uuid.UUID
    x: StatsValues
    y: StatsValues
    z: StatsValues
    period: dict[str, Optional[datetime]]

class UserSchema(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True

class DeviceWithUsersSchema(DeviceSchema):
    users: List[UserSchema] = []

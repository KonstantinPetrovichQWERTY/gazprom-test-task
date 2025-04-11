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
    """Schema for creating new measurement records."""

    x: float
    y: float
    z: float


class PartialUserSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class UserSchema(PartialUserSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class MeasurementSchema(MeasurementCreateSchema):
    """Complete measurement record including metadata."""

    id: uuid.UUID
    device_id: uuid.UUID
    timestamp: datetime

    class Config:
        from_attributes = True


class StatsValues(BaseModel):
    """Statistical summary for a set of measurement values."""

    min: float
    max: float
    count: int
    sum: float
    median: float


class DeviceStatsResponse(BaseModel):
    """Comprehensive statistical analysis for a device's measurements."""

    device_id: uuid.UUID
    x: StatsValues
    y: StatsValues
    z: StatsValues
    period: dict[str, Optional[datetime]]


class DeviceWithUsersSchema(DeviceSchema):
    """Extended device information including associated users."""

    users: List[UserSchema] = []

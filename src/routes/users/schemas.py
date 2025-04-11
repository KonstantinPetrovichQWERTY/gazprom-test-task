from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

from src.routes.devices.schemas import DeviceSchema

class PartialUserSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class UserSchema(PartialUserSchema):
    id: uuid.UUID
    
    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)

class UserWithDevicesSchema(UserSchema):
    devices: List[DeviceSchema] = []

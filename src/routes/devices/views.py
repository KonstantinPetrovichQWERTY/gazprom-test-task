from datetime import datetime
from typing import List, Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import structlog

from src.database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Device, Measurement, User
from src.routes.devices.schemas import DeviceSchema, DeviceStatsResponse, DeviceWithUsersSchema, MeasurementCreateSchema, MeasurementSchema, PartialDeviceSchema
from src.routes.users.schemas import UserSchema


router = APIRouter(tags=["devices"])
logger = structlog.get_logger()


@router.post(
    "/api/v1/devices/register_new_device/",
    response_model=DeviceSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_new_device(
    device_data: PartialDeviceSchema,
    session: AsyncSession = Depends(get_db),
):
    """Register a new device in the system."""

    logger.info("register_new_device: started", device_data=device_data.model_dump())

    # new_coil = await dao.register_new_device(session=session, device_data=device_data)
    existing_device = await session.execute(
        select(Device).where(Device.serial_number == device_data.serial_number))
    if existing_device.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Device with this serial number already exists"
        )
    
    new_device = Device(
        serial_number=device_data.serial_number,
    )

    session.add(new_device)
    await session.commit()
    await session.refresh(new_device)

    logger.info("register_new_device: completed", device_id=new_device.id)
    return new_device


@router.get(
    "/api/v1/devices/",
    response_model=List[DeviceSchema]
)
async def get_all_devices(
    session: AsyncSession = Depends(get_db)
):
    """Get list of all devices with pagination"""
    result = await session.execute(select(Device))
    devices = result.scalars().all()
    return devices


@router.get(
    "/api/v1/devices/{device_id}/",
    response_model=DeviceWithUsersSchema
)
async def get_device(
    device_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    """Get device details by ID"""
    stmt = (
        select(Device)
        .where(Device.id == device_id)
        .options(selectinload(Device.users))
    )
    
    device = (await session.scalars(stmt)).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    result = DeviceWithUsersSchema(
        id=device.id,
        serial_number=device.serial_number,
        users=device.users
    )

    return result


@router.post(
    "/api/v1/devices/{device_id}/measurements/",
    response_model=MeasurementSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_measurement(
    device_id: uuid.UUID,
    measurement_data: MeasurementCreateSchema,
    session: AsyncSession = Depends(get_db)
):
    """Add new measurement for specific device"""
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    measurement = Measurement(
        device_id=device_id,
        timestamp=datetime.now(),
        **measurement_data.model_dump()
    )
    
    session.add(measurement)
    await session.commit()
    await session.refresh(measurement)

    return measurement


@router.get(
    "/api/v1/devices/{device_id}/measurements/",
    response_model=List[MeasurementSchema]
)
async def get_device_measurements(
    device_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    """Get measurements for device with optional date filtering"""
    query = select(Measurement).where(Measurement.device_id == device_id)
    
    if start_date:
        query = query.where(Measurement.timestamp >= start_date)
    if end_date:
        query = query.where(Measurement.timestamp <= end_date)
    
    result = await session.execute(
        query.order_by(Measurement.timestamp.desc())
    )
    measurements = result.scalars().all()

    if not measurements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    return measurements


@router.get(
    "/api/v1/devices/{device_id}/stats/",
    response_model=DeviceStatsResponse
)
async def get_device_stats(
    device_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    """Get statistical analysis for device measurements"""
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    query = select(Measurement).where(Measurement.device_id == device_id)
    if start_date:
        query = query.where(Measurement.timestamp >= start_date)
    if end_date:
        query = query.where(Measurement.timestamp <= end_date)

    result = await session.execute(query)
    measurements = result.scalars().all()

    if not measurements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No measurements found for the specified period"
        )

    x_values = [m.x for m in measurements]
    y_values = [m.y for m in measurements]
    z_values = [m.z for m in measurements]

    def calculate_stats(values):
        sorted_values = sorted(values)
        count = len(sorted_values)
        return {
            "min": min(sorted_values),
            "max": max(sorted_values),
            "count": count,
            "sum": sum(sorted_values),
            "median": sorted_values[count // 2] if count % 2 else 
                     (sorted_values[count // 2 - 1] + sorted_values[count // 2]) / 2
        }

    result = DeviceStatsResponse(
        x=calculate_stats(x_values),
        y=calculate_stats(y_values),
        z=calculate_stats(z_values),
        device_id=device_id,
        period={
            "start": start_date,
            "end": end_date
        }
    )

    return result


@router.post(
    "/api/v1/devices/{device_id}/users/",
    response_model=DeviceWithUsersSchema,
    status_code=status.HTTP_201_CREATED
)
async def add_user_to_device(
    device_id: uuid.UUID,
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    """Add user to device (many-to-many relationship)"""
    device = await session.get(Device, device_id)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )

    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user in device.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already assigned to this device"
        )

    device.users.append(user)
    await session.commit()
    await session.refresh(device)
    return device

@router.get(
    "/api/v1/devices/{device_id}/users/",
    response_model=List[UserSchema]
)
async def get_device_users(
    device_id: uuid.UUID,
    session: AsyncSession = Depends(get_db)
):
    """Get list of users assigned to device"""
    stmt = (
        select(Device)
        .where(Device.id == device_id)
        .options(selectinload(Device.users))
    )
    
    device = (await session.scalars(stmt)).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    result = [UserSchema(id=user.id, name=user.name) for user in device.users]

    return result

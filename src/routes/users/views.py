from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import structlog

from src.database.database import get_db
from src.routes.users.dao import dao
from src.routes.users.schemas import (
    FullUserSchema,
    UserAggregatedStatsResponse,
    UserDeviceStatsResponse,
    UserWithDevicesSchema,
    PartialUserSchema,
)
from src.routes.users.exceptions import (
    UserNotFoundException,
    UserAlreadyExistException,
)

router = APIRouter(tags=["users"])
logger = structlog.get_logger()


@router.post(
    "/api/v1/users/",
    response_model=FullUserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: PartialUserSchema,
    session: AsyncSession = Depends(get_db),
):
    """Create a new user."""
    logger.info("create_user: started", user_data=user_data.model_dump())

    try:
        new_user = await dao.create_user(session=session, user_data=user_data)
    except UserAlreadyExistException as e:
        logger.warning("create_user: User already exists", name=user_data.name)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )

    logger.info("create_user: completed", user_id=new_user.id)
    return new_user


@router.get("/api/v1/users/{user_id}/", response_model=UserWithDevicesSchema)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
):
    """Get user details by ID with associated devices."""
    logger.info("get_user: started", user_id=user_id)

    try:
        user = await dao.get_user(session=session, user_id=user_id)
    except UserNotFoundException as e:
        logger.warning("get_user: User not found", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    logger.info("get_user: completed", user_id=user_id)
    return user


@router.get("/api/v1/users/", response_model=List[FullUserSchema])
async def get_all_users(session: AsyncSession = Depends(get_db)):
    """Get list of all users."""
    logger.info("get_all_users: started")

    users = await dao.get_all_users(session=session)

    logger.info("get_all_users: completed", user_count=len(users))
    return users


@router.get(
    "/api/v1/users/{user_id}/stats/aggregated/",
    response_model=UserAggregatedStatsResponse,
)
async def get_user_aggregated_stats(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    """Get aggregated statistics for all user's devices"""
    logger.info(
        "get_user_aggregated_stats: started",
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    try:
        stats = await dao.get_user_aggregated_stats(
            session=session,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )
    except UserNotFoundException as e:
        logger.warning("get_user_aggregated_stats: User not found", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    logger.info("get_user_aggregated_stats: completed")
    return stats


@router.get(
    "/api/v1/users/{user_id}/stats/devices/",
    response_model=UserDeviceStatsResponse,
)
async def get_user_devices_stats(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
):
    """Get statistics for each user's device separately"""
    logger.info(
        "get_user_devices_stats: started",
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
    )

    try:
        stats = await dao.get_user_devices_stats(
            session=session,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )
    except UserNotFoundException as e:
        logger.warning("get_user_devices_stats: User not found", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    logger.info("get_user_devices_stats: completed")
    return stats

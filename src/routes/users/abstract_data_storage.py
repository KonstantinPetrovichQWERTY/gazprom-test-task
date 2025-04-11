from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes.users.schemas import (
    FullUserSchema,
    UserAggregatedStatsResponse,
    UserDeviceStatsResponse,
    UserWithDevicesSchema,
    PartialUserSchema,
)


class UserDataStorage(ABC):
    """Abstract base class defining operations for user data management."""

    @abstractmethod
    async def create_user(
        self,
        session: AsyncSession,
        user_data: PartialUserSchema,
    ) -> FullUserSchema:
        """Create a new user record in the database."""
        pass

    @abstractmethod
    async def get_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> UserWithDevicesSchema:
        """Retrieve a single user by ID with associated devices."""
        pass

    @abstractmethod
    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> List[FullUserSchema]:
        """Retrieve all users from the database."""
        pass

    @abstractmethod
    async def get_user_aggregated_stats(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> UserAggregatedStatsResponse:
        """Get aggregated statistics for all user's devices"""
        pass

    @abstractmethod
    async def get_user_devices_stats(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> UserDeviceStatsResponse:
        """Get statistics for each user's device separately"""
        pass

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.routes.devices.schemas import DeviceSchema, DeviceStatsResponse, DeviceWithUsersSchema, MeasurementCreateSchema, MeasurementSchema, PartialDeviceSchema
from src.routes.users.schemas import UserSchema


class DeviceDataStorage(ABC):
    """Abstract base class defining operations for device data storage management."""

    @abstractmethod
    async def get_device(
        session: AsyncSession,
        device_id: uuid.UUID,
    ) -> DeviceWithUsersSchema:
        """Retrieve a single device by its unique identifier.

        Args:
            session (AsyncSession): Asynchronous database session
            device_id (uuid.UUID): Unique identifier of the device to retrieve

        Returns:
            DeviceWithUsersSchema: pydantic device schema
        """
        pass

    @abstractmethod
    async def register_new_device(
        session: AsyncSession,
        device_data: PartialDeviceSchema,
    )-> DeviceSchema:
        """Create a new device record in the database.

        Args:
            session (AsyncSession): Asynchronous database session
            device_data (PartialCoilSchema): Required data for device creation

        Returns:
            DeviceSchema: Newly created device with generated ID field
        """
        pass

    @abstractmethod
    async def get_all_devices(
        session: AsyncSession
    ) -> list[DeviceSchema]:
        """Retrieve devices.

        Args:
            session (AsyncSession): Asynchronous database session
            
        Returns:
            list[DeviceSchema]: List of devices
        """
        pass

    @abstractmethod
    async def get_device_stats(
        session: AsyncSession,
        device_id: uuid.UUID,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> DeviceStatsResponse:
        """Calculate aggregate statistics for device within specified time window.

        Args:
            session (AsyncSession): Asynchronous database session
            start_date (Optional[datetime]): Measurements taken after this timestamp
            end_date (Optional[datetime]): Measurements taken before this timestamp

        Returns:
            DeviceStatsResponse: Aggregated statistics
        """
        pass

    @abstractmethod
    async def add_measurement(
        self,
        session: AsyncSession,
        device_id: uuid.UUID,
        measurement_data: MeasurementCreateSchema,
    ) -> MeasurementSchema:
        """Add new measurement for a specific device.

        Args:
            session (AsyncSession): Asynchronous database session
            device_id (uuid.UUID): Device identifier
            measurement_data (MeasurementCreateSchema): Measurement data

        Returns:
            MeasurementSchema: Created measurement
        """
        pass

    @abstractmethod
    async def get_device_measurements(
        self,
        session: AsyncSession,
        device_id: uuid.UUID,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
    ) -> List[MeasurementSchema]:
        """Retrieve measurements for a device with optional time filtering.

        Args:
            session (AsyncSession): Asynchronous database session
            device_id (uuid.UUID): Device identifier
            start_date (Optional[datetime]): Start of time range
            end_date (Optional[datetime]): End of time range

        Returns:
            List[MeasurementSchema]: List of measurements
        """
        pass

    @abstractmethod
    async def add_user_to_device(
        self,
        session: AsyncSession,
        device_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> DeviceWithUsersSchema:
        """Add a user to a device (many-to-many relationship).

        Args:
            session (AsyncSession): Asynchronous database session
            device_id (uuid.UUID): Device identifier
            user_id (uuid.UUID): User identifier

        Returns:
            DeviceWithUsersSchema: Updated device with users
        """
        pass

    @abstractmethod
    async def get_device_users(
        self,
        session: AsyncSession,
        device_id: uuid.UUID,
    ) -> List[UserSchema]:
        """Get list of users assigned to a device.

        Args:
            session (AsyncSession): Asynchronous database session
            device_id (uuid.UUID): Device identifier

        Returns:
            List[UserSchema]: List of users
        """
        pass

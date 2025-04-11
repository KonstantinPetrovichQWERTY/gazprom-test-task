class DeviceNotFoundException(Exception):
    """Custom exception raised when a requested device cannot be located.

    This exception is typically raised during database operations when:
    - Looking up a device by ID that doesn't exist
    - Attempting to update a non-existent device
    - Requesting statistics for a time range with no devices

    Attributes:
        message (str): Human-readable error description. Defaults to
            "Device not found" if not provided explicitly.
    """
    def __init__(self, message: str = "Coil not found"):
        self.message = message
        super().__init__(self.message)


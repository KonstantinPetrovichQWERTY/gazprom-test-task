class UserNotFoundException(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistException(Exception):
    def __init__(self, message: str = "User of this device already exists"):
        self.message = message
        super().__init__(self.message)

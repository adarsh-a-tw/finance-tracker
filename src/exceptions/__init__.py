class TagNotFoundException(Exception):
    def __init__(self):
        super().__init__("Tag is not found in the record.")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Username or password is incorrect.")


class InvalidAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid or missing Authentication token.")

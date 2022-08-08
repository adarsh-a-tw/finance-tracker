class TagNotFoundException(Exception):
    def __init__(self):
        super().__init__("Tag is not found in the record.")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Username or password is incorrect.")


class InvalidAuthTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid or missing Authentication token.")


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__("User not found in database.")


class RecordBookNotFoundException(Exception):
    def __init__(self):
        super().__init__("RecordBook not found in database.")


class PasswordsDontMatchException(Exception):
    def __init__(self):
        super().__init__("Passwords dont match.")


class EmailInvalidException(Exception):
    def __init__(self):
        super().__init__("Email is invalid.")


class UsernameAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Username already exists.")


class EmailAlreadyExistsException(Exception):
    def __init__(self):
        super().__init__("Email already exists.")

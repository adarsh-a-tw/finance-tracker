class TagNotFoundException(Exception):
    def __init__(self):
        super().__init__("Tag is not found in the record.")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Username or password is incorrect.")

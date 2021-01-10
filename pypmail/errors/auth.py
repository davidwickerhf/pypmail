from pypmail.errors.common import ProtonMailException


class InvalidEmailException(ProtonMailException):
    """Raised when inputting an invalid email address
    
    Args:
        user:str: The user's email that caused the exception
    """
    def __init__(self, username:str):
        self.username = username
        super().__init__(message='The email is invalid.')

    def __str__(self):
        return f'{self.username} -> {self.message}'


class SignupFormException(ProtonMailException):
    """Raised when an error occures during signup.
    
    Args:
        username(str): The username used to create the account
        password(str): The password used to create the account
    """
    def __init__(self, username:str, password:str, message:str):
        self.username = username
        self.password = password
        super().__init__(message=message)

    def __str__(self):
        return f'{self.username} | {self.password} -> {self.message}'



class InvaildPasswordException(ProtonMailException):
    """Raised when trying to log in with an incorrect password
    
    Args:
        password:str: The passwod that caused the exception
    """
    def __init__(self, password:str):
        self.password = password
        super().__init__(message='The password used to attempt login is incorrect. Check the password.')


class NotLoggedInException(ProtonMailException):
    """Raised when trying to use a client method without being logged into instagram"""
    def __init__(self):
        super().__init__(message="InstaClient is not logged in.")
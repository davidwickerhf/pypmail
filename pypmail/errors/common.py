"""This module contains common errors and exceptions raised by the ProtonMail"""

class ProtonMailException(Exception):
    """Base ProtonMail Exception

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class InvalidDriverPathExeption(ProtonMailException):
    """Raised when trying to initialize an ProtonMail object on a localhost with an unexisting driver Path.

    Args:
        driver_path
    """
    def __init__(self, driver_path):
        self.driver_path = driver_path
        super().__init__(message='No driver was found in the indicated path')

    def __str__(self):
        return f'{self.driver_path} -> {self.message}'



class InvaildHostException(ProtonMailException):
    """Raised when trying to pass an incorrect host index in ProtonMail.__init__()

    Args:
        host_int:int: The driver int variable passed to ProtonMail()
    """
    def __init__(self, host_int:int):
        self.host_int = host_int
        super().__init__(message='This integer does not refer to any host type')

    def __str__(self):
        return f'{self.host_int} -> {self.message}'
    


class InvaildDriverException(ProtonMailException):
    """Raised when trying to pass an incorrect driver index in ProtonMail.__init__()

    Args:
        driver_int:int: The driver int variable passed to ProtonMail()
    """
    def __init__(self, driver_int:int):
        self.driver_int = driver_int
        super().__init__(message='This integer does not refer to any driver')

    def __str__(self):
        return f'{self.driver_int} -> {self.message}'


class InvalidErrorCallbackException(ProtonMailException):
    """Raised when initiating an ProtonMail object if the `error_callback` argument is provided but is not a callable object.
    """
    def __init__(self):
        super().__init__(message='The error callback you provided is not a callable.')


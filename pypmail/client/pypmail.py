from selenium.webdriver.remote.webdriver import WebDriver
from pypmail.client import *

# Import Class Modules
#from pypmail.client.auth import PMAuth

class ProtonMail(PMAuth):
    def __init__(self, driver_path:str=None, localhost:bool=True, show_driver:bool=False, proxy:str=None, logger:logging.Logger=None, error_callback=None, debug:bool=True, **callback_args) -> None:
        if localhost and not driver_path:
            raise InvalidDriverPathExeption(driver_path)

        self.driver_path = driver_path
        self.debug = debug
        if error_callback:
            if not callable(error_callback):
                raise InvalidErrorCallbackException()

        self.localhost = localhost
        self.error_callback = error_callback 
        self.error_callback_args = callback_args
        self.show_driver = show_driver
        self.proxy = proxy
        self.driver:WebDriver = None
        self.email = None
        self.password = None

        global LOGGER
        if logger:
            LOGGER = logger

        if debug and not logger:
           LOGGER.setLevel(logging.DEBUG)

    # CLIENT PROPERTIES
    @property
    def logged_in(self) -> bool:
        """Checks whether the client is currently logged in to ProtonMail.com.

        Returns:
            bool: True if `driver` is open and user is logged into ProtonMail.com.
        """
        if self.driver:
            if self.email and self.password:
                url = self.driver.current_url
                if 'https://www.protonmail.com/' in url and ClientUrls.LOGIN_URL not in url:
                    return True
        return False

    @property
    def threads(self) -> Optional[list]:
        """gets all the threads created and controlled by the client. All such threads include `instaclient` in their names.

        Returns:
            Optional[list]: A list of all sub-threads created and controlled by the client. Returns `None` if no thread is found.
        """
        running = list()
        for thread in threading.enumerate(): 
            if thread is not threading.main_thread() and 'pypmail' in thread.getName():
                running.append(thread)
        
        if len(running) < 1:
            return None
        else:
            return running



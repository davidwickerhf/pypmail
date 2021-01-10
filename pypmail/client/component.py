from pypmail.client import *
if TYPE_CHECKING:
    from pypmail.client.pypmail import ProtonMail

class PMComponent:
    
    def _login_required(func):
        @wraps(func)
        def wrapper(self: 'ProtonMail', *args, **kwargs):
            if self.username is None or self.password is None:
                    raise NotLoggedInException()

            if not self.logged_in:
                if not self.driver:
                    self.connect(True, func=func.__name__)
                else:
                    self.login(self.email, self.password)

            error = False
            result = None
            try:
                result = func(self, *args, **kwargs)
            except Exception as exception:
                error = exception
            
            time.sleep(randint(1, 2))
            if error:
                raise error
            else:
                return result
        return wrapper


    def _driver_required(func):
        @wraps(func)
        def wrapper(self: 'ProtonMail', *args, **kwargs):
            if not self.driver:
                self.connect(func=func.__name__)

            error = False
            result = None
            try:
                result = func(self, *args, **kwargs)
            except Exception as exception:
                error = exception
            
            time.sleep(randint(1, 2))
            if error:
                raise error
            else:
                return result
        return wrapper


    def disconnect(self: 'ProtonMail'):
        """Disconnects the client from ProtonMail

        If ``client.driver`` is not None, the currently connected Web Driver
        will be closed and discarded.
        """
        LOGGER.debug('ProtonMail: Discarding driver...')
        if self.driver:
            self.driver.quit()
            self.driver = None
        LOGGER.debug('ProtonMail: Driver Discarded')


    def connect(self: 'ProtonMail', retries=0, func=None):
        """Connects the client to Instagram

        if ``ProtonMail.driver`` is None, a new connection will be created
        with the ChromeDriver. This means a new chrome window will be
        opened.

        Args:
            retries (int, optional): Defines the number of times to
                retry connecting to the web driver before raising
                an error. Defaults to 0.
            func (str, optional): The name of the method where the 
                `connect` method is called. This is used for debugging
                purposes and is usually passed automatically by the decorators
                :meth:`ProtonMail.ProtonMail._driver_required` and
                :meth:`ProtonMail.ProtonMail._login_required`. Defaults to None.

        Returns:
            :class:`pypmail.ProtonMail`: if a connection to the website is
                established successfully, the connected client will be 
                returned.

        Raises:
            WebDriverException: This is raised if an error occures when
                launching the WebDriver and connecting with Selenium.
            ProtonMailError: This is raised if an error occures when trying to
                log in - if the `login` attribute is set to be True.
        """
        LOGGER.debug('ProtonMail: Initiating Driver | attempt {} | func: {}'.format(retries, func))
        try:
            if not self.localhost:
                # Running on web server
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-setuid-sandbox") 
                chrome_options.add_argument("--remote-debugging-port=9222")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                if self.proxy:
                    chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            else:
                # Running locally
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument("--headless") if not self.show_driver else None
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                LOGGER.debug('Path: {}'.format(self.driver_path))
                if self.proxy:
                    chrome_options.add_argument('--proxy-server=%s' % self.proxy)
                
                self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)

        except WebDriverException as error:
            if retries < 2:
                LOGGER.debug('ProtonMail: Error when initiating driver... Trying again')
                self.connect(retries=retries+1, func='_connect')
            else:
                raise error


    # PM PRIVATE UTILITIES (The client is considered initiated)
    def _find_element(self:'ProtonMail', expectation, url:str=None, wait_time:int=5, retry=True, attempt=0):
        """Finds and returns the `WebElement`(s) that match(es) the expectation's XPATH.

        If the element is not found within the span of time defined by the 
        `wait_time` attribute, the method will check if a few conditions are met, 
        in which case it will call itself again if `retry` is set to True

        Args:
            expectation (:class:expected_conditions): Any class 
                defined in ``selenium.webdriver.support.expected_conditions``
            url (str): The url at which the element is expected to be present
            wait_time (int, optional): Time in seconds to wait to find the element. 
                Defaults to 5 seconds.
            attempt (int, optional): Number of failed attempts. 
                Note:
                    Do not insert a custom value for this attribute, leave it to 0.

        Raises:
            NoSuchElementException: Raised if the element is not found after two attempts.

        Returns:
            :class:`WebElement`: web element that matches the `expectation` xpath
        """
        try:
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            if widgets == None:
                raise NoSuchElementException()
            else:
                return widgets
        except TimeoutException:
            # Element was not found in time
            LOGGER.debug('ProtonMail: Element Not Found...')
            if retry and attempt < 2:
                LOGGER.debug('Retrying find element...')
                LOGGER.debug('Checking if user is logged in...')
                #self.driver.get(url)
                return self._find_element(expectation, url, wait_time=2, attempt=attempt+1)

            else:
                if self.error_callback:
                        self.error_callback(self.driver)
                LOGGER.exception('The element with locator {} was not found'.format(expectation.locator))
                raise NoSuchElementException()


    def _check_existence(self:'ProtonMail', expectation, wait_time:int=2):
        """
        Checks if an element exists.
        Args:
            expectation: EC.class
            wait_time:int: (Seconds) retry window before throwing Exception
        """
        try: 
            wait = WebDriverWait(self.driver, wait_time)
            widgets = wait.until(expectation)
            return True
        except:
            return False

    
    def _press_button(self, button):
        try:
            button.click()
            time.sleep(randrange(0,2))
            return True
        except:
            return False
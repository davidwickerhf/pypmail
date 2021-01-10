import typing
from selenium.webdriver.remote.webdriver import _W3C_CAPABILITY_NAMES

from selenium.webdriver.support.expected_conditions import presence_of_element_located
from pypmail.client import *
if TYPE_CHECKING:
    from pypmail.client.pypmail import ProtonMail


class PMAuth(PMNavigator):
    FREE_PLAN = 1

    CONFIRM_VIA_SMS = 1
    CONFIRM_VIA_EMAIL = 2

    def signup(self:'ProtonMail', username:str, password:str, recovery_email:str=None, plan:int=FREE_PLAN, confirmation_type:int=CONFIRM_VIA_EMAIL, confirmation_phone:str=None, confirmation_email:str=None):
        # Check if correct confirmation arguments are provided
        if confirmation_type == PMAuth.CONFIRM_VIA_EMAIL and not confirmation_email:
            raise SignupFormException(username, password, 'Confirmation type CONFIRM_VIA_EMAIL requires a valid confirmation_email argument')
        elif confirmation_type == PMAuth.CONFIRM_VIA_SMS and not confirmation_phone:
            raise SignupFormException(username, password, 'Confirmation type CONFIRM_VIA_PHONE requires a valid confirmation_phone argument in international format')

        # Navigate to Signup Page
        result = self._nav_signup_page()
        if not result:
            raise ProtonMailException(f'Error in loading signup page: {self.driver.current_url}')
        LOGGER.debug('Got SignUp page')

        # Select Plan
        if plan == PMAuth.FREE_PLAN:
            # FREE PLAN
            plan_div = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FREE_PLAN_DIV)))
            self._press_button(plan_div)
            time.sleep(1.5)

            # Press Free Plan Button
            select_plan = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.FREE_PLAN_BTN)))
            self._press_button(select_plan)
        LOGGER.debug('Selected account plan')

        # The page should load at this point - it might take a while
        username_input = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_USERNAME)), wait_time=4)
        username_input.send_keys(username)
        LOGGER.debug('Inputted username')
        time.sleep(0.5)

        # Input Password
        first_password_input = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_FIRST_PASSWORD)))
        first_password_input.send_keys(password)
        LOGGER.debug('Inputted password')
        time.sleep(0.5)

        second_password_input = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_SECOND_PASSWORD)))
        second_password_input.send_keys(password)
        LOGGER.debug('Inputted password confirmation')
        time.sleep(0.5)

        # Input recovery email
        if recovery_email:
            recovery_email_input = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_RECOVERY_EMAIL)))
            recovery_email_input.send_keys(recovery_email)
            LOGGER.debug('Inputted recovery email')


        # Submit Form
        submit = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.CREATE_ACCOUNT_BTN)))
        self._press_button(submit)
        LOGGER.debug('Submitted form')

        # Check for invalid Username
        result = self._check_existence(EC.presence_of_element_located((By.XPATH, Paths)), wait_time=3)
        if result:
            error:WebElement = self._find_element(EC.presence_of_element_located((By.XPATH, Paths)))
            error_text = error.text
            raise SignupFormException(username, password, error_text)

        # Successful Form Submition
        # Select Confirmation Type
        if confirmation_type is PMAuth.CONFIRM_VIA_SMS:
            confirm_type_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_SMS_VERIFICATION)))
            input_locator = (By.XPATH, Paths.SIGNUP_VERIFICATION_SMS_INPUT)
            input_text = confirmation_phone
        else:
            confirm_type_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_EMAIL_VERIFICATION)))
            input_locator = (By.XPATH, Paths.SIGNUP_VERIFICATION_EMAIL_INPUT)
            input_text = confirmation_email
        self._press_button(confirm_type_btn)
        LOGGER.debug('Selected verification type')
        time.sleep(0.5)

        confirm_input = self._find_element(EC.presence_of_element_located(input_locator))
        confirm_input.send_keys(input_text)
        LOGGER.debug('Inputted confirmation credentials')

        confirm_btn = self._find_element(EC.presence_of_element_located((By.XPATH, Paths.SIGNUP_CONFIRM_BTN)))
        self._press_button(confirm_btn)
        LOGGER.debug('Sent form')
        return self


    def input_confirmation_code(self):
        pass


    def send_new_confirmation_code(self):
        pass


    def change_confirmation_email(self):
        pass


    def login():
        pass


    def logout():
        pass




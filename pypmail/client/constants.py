class ClientUrls:
    SIGNUP_URL = 'https://protonmail.com/signup'


class APIUrls:
    pass


class Paths:
    # GENERAL
    ERROR_PAGE_DIV = '//body[@class="error404"]'
    
    # AUTH MODULE ##########################################################################
    # SIGNUP METHOD
    # plans divs
    FREE_PLAN_DIV = '//div[@class="panel-heading collapsed" and @aria-controls="plan-free"]'
    # select plan buttons
    FREE_PLAN_BTN = '//button[@id="freePlan"]'
    # Signup Form
    SIGNUP_USERNAME = '/html/body/div/div/div/div/input'
    SIGNUP_FIRST_PASSWORD = '//div[@class="margin usernamePassword-field-password"]//descendant::input'
    SIGNUP_SECOND_PASSWORD = '//div[@class="margin usernamePassword-field-password-confirm"]//descendant::input'
    SIGNUP_RECOVERY_EMAIL = '//input[@id="notificationEmail"]'
    CREATE_ACCOUNT_BTN = '//button[@type="submit"]'
    FORM_ERROR = '//div[@class="error"]'
    # Verification Block
    SIGNUP_EMAIL_VERIFICATION = '//div[@class="humanVerification-block-email"]'
    SIGNUP_SMS_VERIFICATION = '//div[@class="humanVerification-block-sms"]'
    SIGNUP_VERIFICATION_SMS_INPUT = '//input[@id="smsVerification"]'
    SIGNUP_VERIFICATION_EMAIL_INPUT = '//input[@id="emailVerification"]'
    SIGNUP_CONFIRM_BTN = '//button[@type="submit"]'


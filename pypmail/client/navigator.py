from pypmail.client import *
if TYPE_CHECKING:
    from pypmail.client.pypmail import ProtonMail


class PMNavigator(PMCheckers):

    @PMComponent._driver_required
    def _nav_signup_page(self:'ProtonMail'):
        # Get Page
        self.driver.get(ClientUrls.SIGNUP_URL)

        # Check page Vadility
        return self._is_valid_page(ClientUrls.SIGNUP_URL)

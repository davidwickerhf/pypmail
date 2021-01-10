from pypmail.client import *
if TYPE_CHECKING:
    from pypmail.client.pypmail import ProtonMail


class PMCheckers(PMComponent):

    @PMComponent._driver_required
    def _is_valid_page(self:'ProtonMail', url:str=None):
        """Checks if a page is valid.

        Args:
            url (str, optional): Expected current url. Defaults to None.

        Returns:
            bool: True if the current page exists and is loaded.
                False if the current url doesn\'t match the expected
                url or if a PAGE NOT FOUND warning is showed
                on the page itself.
        """
        current = self.driver.current_url
        if url:
            if url != current:
                self.driver.get(url)
                current = self.driver.current_url

        if url and current != url:
            return False

        if self._check_existence(EC.presence_of_element_located((By.XPATH, Paths.ERROR_PAGE_DIV)), wait_time=2):
            return False

        return True
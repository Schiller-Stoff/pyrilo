import logging

from selenium import webdriver
from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.api.auth.AuthCookie import AuthCookie
from urllib3 import request
from urllib3.exceptions import NameResolutionError


class AuthorizationServiceSelenium:
    """
    Outdated authorization service using selenium to authenticate against the gams-api.
    """

    host: str
    auth_cookie: AuthCookie | None = None

    def __init__(self, host):
        # self.user = user
        # self.password = password
        self.host = host


    def verify_oauth_workflow_works(self):
        """
        Checks if the authentication endpoint is reachable AND if the redirection workflow (oatuh2) works
        as expected.
        1. Try to reach the auth endpoint
        2. Retry logic following redirects
        3. If not reachable, raise ConnectionError
        """
        auth_url = self.host + PyriloStatics.AUTH_ENDPOINT
        # use cookie header if available
        try:
            r = request("GET", auth_url, retries=3, redirect=True)
        except Exception as e:
            # if cause is of type NameResolutionError, append cause info
            # check if cause is a NameResolutionError
            if(isinstance(e.__cause__, NameResolutionError)):
                msg = f"Failed to reach auth service endpoint at {auth_url} due to NameResolutionError. You must set 'keycloak' to resolve against localhost on your local machine - otherwise the ouath2 redirection workflow is not going to work! Original Exception: {e}"
                raise ConnectionError(msg)

            logging.error(msg)
            msg = f"Failed to reach auth service endpoint at {auth_url}. Exception: {e}"
            raise ConnectionError(msg)

        if r.status >= 400:
            msg = f"Failed to reach auth service endpoint at {auth_url}. Status: {r.status}. Response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Auth service endpoint reachable at: {auth_url}")

    def login(self):
        self.verify_oauth_workflow_works()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome(options=chrome_options)

        # open the selenium browser
        driver.get(self.host + PyriloStatics.AUTH_ENDPOINT)
        # need to append a trailing slash to the host url

        # TODO could I check if cookies are still valid? maybe no login is required.

        redirect_url = self.host + "/"
        # wait until redirection to login page is finished
        while not driver.current_url == redirect_url:
            pass

        # TODO there is a driver.get_cookie method!
        cookies = driver.get_cookies()

        # TODO elaborate error handling
        JSESSION_ID = driver.get_cookie("JSESSIONID").get("value")

        self.auth_cookie = AuthCookie(JSESSION_ID)
        # close browser again
        driver.close()
        return self.auth_cookie

    def retrieve_auth_cookie(self):
        if not self.auth_cookie:
            return self.login()
        return self.auth_cookie


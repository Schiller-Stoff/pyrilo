from selenium import webdriver

from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.api.auth.AuthCookie import AuthCookie


class AuthorizationService:

    host: str
    auth_cookie: AuthCookie | None = None

    def __init__(self, host):
        # self.user = user
        # self.password = password
        self.host = host

    def login(self):
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

        # todo there is a driver.get_cookie method!
        cookies = driver.get_cookies()

        JSESSION_ID = ""
        # Print the cookies
        for cookie in cookies:
            if cookie.get('name') == 'JSESSIONID':
                JSESSION_ID = cookie.get('value')
            else:
                # TODO error handling
                pass

        # TODO error handling if JSESSION_ID is still empty


        self.auth_cookie = AuthCookie(JSESSION_ID)
        # close browser again
        driver.close()
        return self.auth_cookie

    def retrieve_auth_cookie(self):
        if not self.auth_cookie:
            return self.login()
        return self.auth_cookie


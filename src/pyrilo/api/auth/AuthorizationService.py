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


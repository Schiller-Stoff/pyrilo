from selenium import webdriver

from pyrilo.auth.AuthCookie import AuthCookie


class AuthorizationService:

    host: str
    auth_cookie: AuthCookie | None = None

    def __init__(self, host):
        # self.user = user
        # self.password = password
        self.host = host

    def login(self):
        driver = webdriver.Chrome()
        # open the selenium browser
        driver.get(self.host)
        # wait until the user logs in and gets redirected to the spring security redirect page
        input("[ Press Enter] after you have logged in and have been redirected to the spring security redirect page...")
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





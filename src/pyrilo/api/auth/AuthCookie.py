

class AuthCookie:

    _JSESSION_COOKIE_VALUE: str

    def __init__(self, jsession_cookie_value):
        self._JSESSION_COOKIE_VALUE = jsession_cookie_value

    def build_auth_cookie_header(self):
        return {'Cookie': f'JSESSIONID={self._JSESSION_COOKIE_VALUE}'}

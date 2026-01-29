import logging
import requests
from urllib.parse import urljoin
from getpass import getpass
from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.api.auth.LoginFormParser import LoginFormParser


class AuthorizationService:
    def __init__(self, session: requests.Session, host: str):
        self.session = session
        self.host = host

    def login(self, username: str = None, password: str = None) -> None:
        """
        Performs authentication. The session cookies are updated automatically.
        """
        login_url = f"{self.host}{PyriloStatics.AUTH_ENDPOINT}"

        # Mimic a browser to avoid bot detection or simplified HTML responses
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        try:
            # 1. Get the login page (requests handles redirects automatically by default)
            response = self.session.get(login_url, headers=headers)
            response.raise_for_status()

            # 2. Parse the login form
            parser = LoginFormParser()
            parser.feed(response.text)

            if not parser.action:
                raise ValueError("Could not find a login form action URL.")

            # TODO unclear - what is with http redirects? - should throw
            action_url = parser.action
            if not action_url.startswith('http'):
                action_url = urljoin(response.url, action_url)

            # 3. Get Credentials
            if not username:
                print(f"Logging in to {self.host}")
                username = input("Username: ")
                password = getpass("Password: ")

            # 4. Prepare Payload
            payload = {
                'username': username,
                'password': password,
                'credentialId': ''
            }
            # Add hidden inputs (CSRF, execution tokens) found by the parser
            payload.update(parser.hidden_inputs)

            # 5. Submit Form
            logging.info("Submitting credentials...")
            # We use the SAME session, so cookies from step 1 are included
            post_response = self.session.post(action_url, data=payload, headers=headers)
            post_response.raise_for_status()

            # 6. Verify Login
            # Check if we have the session cookie or if we are still on the login page
            # (Simplest check: did we get a JSESSIONID?)
            if "JSESSIONID" not in self.session.cookies:
                # Some servers use different cookie names, but GAMS usually uses JSESSIONID.
                # If strictly required, check logic here.
                logging.warning("Login completed, but JSESSIONID cookie not found in session.")
            else:
                logging.info("Successfully logged in and session established.")

        except requests.RequestException as e:
            logging.error(f"Login failed: {e}")
            raise ConnectionError(f"Login failed: {e}")
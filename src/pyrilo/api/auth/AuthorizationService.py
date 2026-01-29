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
        Performs authentication.
        Raises PermissionError if credentials are rejected.
        """
        login_url = f"{self.host}{PyriloStatics.AUTH_ENDPOINT}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            # 1. Get the login page
            response = self.session.get(login_url, headers=headers)
            response.raise_for_status()

            # 2. Parse the login form
            parser = LoginFormParser()
            parser.feed(response.text)

            if not parser.action:
                # If we can't find a form, we might already be logged in.
                # But if we intended to login and can't find a form, it's safer to warn.
                logging.warning("No login form found. Assuming already authenticated or non-standard page.")
                return

            action_url = parser.action
            if not action_url.startswith('http'):
                action_url = urljoin(response.url, action_url)

            # 3. Get Credentials
            if not username:
                print(f"Logging in to {self.host}")
                username = input("Username: ")
                password = getpass("Password: ")

            # 4. Submit Form
            payload = {'username': username, 'password': password, 'credentialId': ''}
            payload.update(parser.hidden_inputs)

            logging.info("Submitting credentials...")

            # Post request
            post_response = self.session.post(action_url, data=payload, headers=headers)

            # --- VALIDATION LOGIC START ---

            # Check 1: HTTP Error Codes (401/403)
            if post_response.status_code >= 400:
                raise PermissionError(f"Login failed with status {post_response.status_code}.")

            # Check 2: "error" in URL (Common Spring/Java pattern: /login?error)
            if "error" in post_response.url.lower():
                raise PermissionError("Login failed: Invalid credentials (server returned error param).")

            # Check 3: Did we land back on the login page?
            # If the response still contains a password input field, the server likely re-rendered the form.
            if 'type="password"' in post_response.text.lower():
                raise PermissionError("Login failed: Login form detected in response content.")

            # --- VALIDATION LOGIC END ---

            logging.info("Login successful (session cookie established).")

        except requests.RequestException as e:
            raise ConnectionError(f"Login network failure: {e}")
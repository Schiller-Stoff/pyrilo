import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from getpass import getpass
from pyrilo.api.auth.AuthCookie import AuthCookie
from pyrilo.PyriloStatics import PyriloStatics


class AuthorizationService:
    def __init__(self, host):
        self.host = host
        self.session = requests.Session()

    def login(self, username: str = None, password: str = None) -> AuthCookie:
        """
        Performs headless authentication using requests.
        """
        login_url = f"{self.host}{PyriloStatics.AUTH_ENDPOINT}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            # 1. Request the Auth Endpoint, but STOP before following the redirect
            response = self.session.get(login_url, headers=headers, allow_redirects=False)

            # 2. Check if we got the expected redirect
            if response.status_code in (301, 302, 303, 307, 308):
                redirect_url = response.headers.get('Location')

                # CRITICAL FIX: If server downgrades to HTTP but we started with HTTPS, force HTTPS.
                if redirect_url and redirect_url.startswith("http://") and self.host.startswith("https://"):
                    logging.warning(f"Detected insecure redirect to {redirect_url}. Upgrading to HTTPS.")
                    redirect_url = redirect_url.replace("http://", "https://", 1)

                # 3. Now follow the corrected URL (and allow subsequent redirects normally)
                response = self.session.get(redirect_url, headers=headers)

            # Raise error if the final landing page (or the initial one if no redirect) failed
            response.raise_for_status()

        except requests.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                logging.error(f"Failed URL: {e.response.url}")
                logging.error(f"Status Code: {e.response.status_code}")
                logging.error(f"Response Body Snippet: {e.response.text[:200]}")
            raise ConnectionError(f"Failed to reach auth endpoint: {e}")

        # 2. Parse the login form to get the dynamic 'action' URL
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        if not form:
            raise ValueError(
                "Could not find login form on the page. The service might not be using a standard HTML form.")

        action_url = form.get('action')
        # Handle relative URLs
        if not action_url.startswith('http'):
            action_url = urljoin(response.url, action_url)

        # 3. Prompt for credentials if not provided
        if not username:
            print(f"Logging in to {self.host}")
            username = input("Username: ")
            password = getpass("Password: ")

        # 4. Submit the form
        # Note: You might need to scrape hidden input fields (like CSRF tokens) from the 'form'
        # and include them in this payload.
        payload = {'username': username, 'password': password, 'credentialId': ''}

        # Add any hidden fields required by Keycloak
        for input_tag in form.find_all('input'):
            if input_tag.get('type') == 'hidden':
                payload[input_tag.get('name')] = input_tag.get('value')

        logging.info("Submitting credentials...")
        post_response = self.session.post(action_url, data=payload)

        if post_response.status_code >= 400:
            raise PermissionError("Login failed. Check credentials or server logs.")

        # 5. Extract the cookie from the session
        return self._extract_cookie()

    def _extract_cookie(self):
        # Look for JSESSIONID in the session cookies
        cookie_val = self.session.cookies.get("JSESSIONID")
        if not cookie_val:
            raise ValueError("Authentication successful, but JSESSIONID cookie was not found.")

        logging.info("Successfully retrieved JSESSIONID.")
        return AuthCookie(cookie_val)
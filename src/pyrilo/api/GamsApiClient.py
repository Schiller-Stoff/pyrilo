import logging
import requests
from typing import Optional
from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.exceptions import PyriloAuthenticationError, PyriloPermissionError, PyriloNotFoundError, \
    PyriloConflictError, PyriloApiError, PyriloNetworkError


class GamsApiClient:
    """
    Owns the HTTP session and handles all low-level API interactions.
    """
    session: requests.Session
    host: str
    api_base_url: str

    def __init__(self, host: str):
        # 1. Initialize Session internally
        self.session = requests.Session()

        # 2. Configure Headers (Moved from Pyrilo.py)
        self.session.headers.update({
            "User-Agent": "Pyrilo (Research Software)",
            "Accept": "application/json"
        })

        self.host = host.rstrip("/")
        self.api_base_url = f"{self.host}{PyriloStatics.API_ROOT}"

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("DELETE", endpoint, **kwargs)

    def head(self, endpoint: str, **kwargs) -> requests.Response:
        return self._request("HEAD", endpoint, **kwargs)

    def _request(self, method: str, endpoint: str, raise_errors: bool = True, **kwargs) -> requests.Response:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{self.api_base_url}/{endpoint.lstrip('/')}"

        logging.debug(f"Requesting {method} {url} ...")

        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as e:
            # Context: This is a low-level network failure (DNS, Timeout)
            msg = f"Network failure connecting to {url}: {e}"
            logging.error(msg)
            raise PyriloNetworkError(msg) from e

        if raise_errors:
            self._handle_error_status(response)

        return response

    def _handle_error_status(self, response: requests.Response):
        """Maps HTTP status codes to Pyrilo exceptions."""
        if response.status_code < 400:
            return

        code = response.status_code
        msg = f"API Error {code} for {response.url}: {response.text}"

        logging.error(msg)

        if code == 401:
            raise PyriloAuthenticationError(msg, code, response.text)
        elif code == 403:
            raise PyriloPermissionError(msg, code, response.text)
        elif code == 404:
            raise PyriloNotFoundError(msg, code, response.text)
        elif code == 409:
            raise PyriloConflictError(msg, code, response.text)
        else:
            # Fallback for 500s or other 4xx
            raise PyriloApiError(msg, code, response.text)
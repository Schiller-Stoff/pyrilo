import logging
import requests
from pyrilo.PyriloStatics import PyriloStatics

class GamsApiClient:
    """
    Central client for handling HTTP interactions with the GAMS5 API.
    Wraps requests to handle URL construction, logging, and common error checking.
    """

    def __init__(self, session: requests.Session, host: str):
        self.session = session
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
        """
        Internal wrapper for requests.
        :param endpoint: relative path from api root OR absolute url starting with httpö
        """

        if endpoint.startswith("http://"):
            logging.warning(f"Found insecure http:// call in GamsApiClient. http:// should not be used in production:  {endpoint}")

        # Refactoring: Support absolute URLs for Auth redirects/actions
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            url = f"{self.api_base_url}/{endpoint.lstrip('/')}"

        logging.debug(f"Requesting {method} {url} ...")

        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as e:
            msg = f"Network failure connecting to {url}: {e}"
            logging.error(msg)
            raise ConnectionError(msg)

        if raise_errors and response.status_code >= 400:
            msg = f"Failed to request {method} {url}. Status: {response.status_code}. Response: {response.text}"
            logging.error(msg)
            raise ConnectionError(msg)

        return response
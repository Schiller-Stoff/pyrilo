class PyriloError(Exception):
    """Base exception for all Pyrilo errors. Catch this to handle any app-specific failure."""
    pass

class PyriloConfigurationError(PyriloError):
    """Raised when the application is misconfigured (e.g. missing generic environment variables)."""
    pass

class PyriloNetworkError(PyriloError):
    """Raised when the server cannot be reached (DNS, Timeout, Connection Refused)."""
    pass

class PyriloApiError(PyriloError):
    """Base for HTTP 4xx/5xx errors returned by the API."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text

class PyriloAuthenticationError(PyriloApiError):
    """Raised for 401 Unauthorized (Login failed)."""
    pass

class PyriloPermissionError(PyriloApiError):
    """Raised for 403 Forbidden (User lacks rights)."""
    pass

class PyriloNotFoundError(PyriloApiError):
    """Raised for 404 Not Found."""
    pass

class PyriloConflictError(PyriloApiError):
    """Raised for 409 Conflict (e.g., Object already exists)."""
    pass
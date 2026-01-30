import pytest
import requests
from unittest.mock import MagicMock
from pyrilo.api.GamsApiClient import GamsApiClient
from pyrilo.exceptions import (
    PyriloAuthenticationError,
    PyriloPermissionError,
    PyriloNotFoundError,
    PyriloConflictError,
    PyriloApiError
)


@pytest.fixture
def client_with_mock_session():
    client = GamsApiClient("http://mock-host")
    client.session = MagicMock(spec=requests.Session)
    return client


@pytest.mark.parametrize("status_code, exception_class", [
    (401, PyriloAuthenticationError),
    (403, PyriloPermissionError),
    (404, PyriloNotFoundError),
    (409, PyriloConflictError),
    (500, PyriloApiError),
    (418, PyriloApiError),  # Teapot / Unhandled 4xx
])
def test_error_handling_mapping(client_with_mock_session, status_code, exception_class):
    """
    Verifies that specific HTTP status codes raise the specific Pyrilo exceptions.
    """
    # Setup the mock response
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = status_code
    mock_response.text = "Error Message"
    mock_response.url = "http://mock-host/api"

    # Make the session return this response
    client_with_mock_session.session.request.return_value = mock_response

    # Act & Assert
    with pytest.raises(exception_class) as exc_info:
        client_with_mock_session.get("some-endpoint")

    # Verify the error message contains context
    assert f"API Error {status_code}" in str(exc_info.value)


def test_successful_request_no_error(client_with_mock_session):
    """
    Verifies that 200 OK does NOT raise an exception.
    """
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    client_with_mock_session.session.request.return_value = mock_response

    try:
        client_with_mock_session.get("some-endpoint")
    except PyriloApiError:
        pytest.fail("Client raised PyriloApiError on 200 OK response")
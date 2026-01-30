import pytest
from unittest.mock import MagicMock, patch

from utils.TestPyriloProject import TestPyriloProject


@pytest.fixture
def mock_gams_api():
    """
    Patches the low-level requests.Session.request method.
    This intercepts ALL HTTP calls made by pyrilo (Login, Head, Post, etc.)
    and simulates a successful GAMS server.
    """
    with patch("requests.Session.request") as mock_request:
        # Define a side_effect function to handle different endpoints dynamically
        def api_side_effect(method, url, **kwargs):
            # Create a generic successful response mock
            response = MagicMock()
            response.status_code = 200
            response.text = "<html>Login Form</html>"
            response.url = url

            # 1. Handle Login (GET auth)
            if "auth" in url and method == "GET":
                # Returns a fake login form that your parser will accept
                response.text = '<form action="/login-action"><input type="hidden" name="execution" value="123"/></form>'
                return response

            # 2. Handle Login Submission (POST login-action)
            if "login-action" in url and method == "POST":
                # Simulate successful login redirect
                response.url = "http://test-gams.local/home"
                return response

            # 3. Handle Object Existence Check (HEAD objects/{id})
            if f"objects" in url and method == "HEAD":
                # Simulate that the object does NOT exist yet (so we don't try to delete it)
                response.status_code = 404
                return response

            # 4. Handle Ingest (POST objects)
            if "objects" in url and method == "POST":
                response.status_code = 201  # Created
                return response

            # Default for anything else
            return response

        mock_request.side_effect = api_side_effect
        yield mock_request

@pytest.fixture
def test_pyrilo_ingest_files(tmp_path):
    """
    Setup procedure for pyrilo ingest files
    Could create random files etc.
    """
    return TestPyriloProject()

@pytest.fixture
def mock_pyrilo_ingest_env(mock_gams_api, test_pyrilo_ingest_files):
    """
    Sets up a complete pyrilo ingest environment with mocked gams-api and available test data
    """
    return mock_gams_api, test_pyrilo_ingest_files

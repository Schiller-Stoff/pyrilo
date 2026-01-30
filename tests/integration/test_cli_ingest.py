from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

# Import your actual entry point
from pyrilo.cli import cli

# --- Test Data & Configuration ---
TEST_PROJECT = "demo_project"
TEST_BAG_NAME = f"{TEST_PROJECT}_bag_001"
MOCK_HOST = "http://test-gams.local"


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
            if f"objects/{TEST_BAG_NAME}" in url and method == "HEAD":
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


def test_cli_ingest_flow_success(tmp_path, mock_gams_api):
    """
    INTEGRATION TEST:
    1. Sets up a real temporary file structure.
    2. Runs the real 'pyrilo ingest' CLI command.
    3. Mocks only the network responses.

    Proofs:
    - CLI argument parsing works.
    - Authentication flow works.
    - FileSystem service correctly finds and zips files.
    - IngestService correctly constructs the API request.
    """

    # 1. Setup: Create a fake bag structure in a temporary directory
    # Structure: /tmp/bags/demo_project_bag_001/data.txt
    bags_root = tmp_path / "bags"
    bag_folder = bags_root / TEST_BAG_NAME
    bag_folder.mkdir(parents=True)
    (bag_folder / "data.txt").write_text("Hello GAMS")

    # 2. Act: Run the CLI command
    runner = CliRunner()

    # We pass credentials via env vars to avoid CLI prompts
    env_vars = {
        "PYRILO_USER": "testuser",
        "PYRILO_PASSWORD": "testpass"
    }

    result = runner.invoke(
        cli,
        [
            "--host", MOCK_HOST,
            "--bag_root", str(bags_root),  # Point to our temp dir
            "--verbose",
            "ingest", TEST_PROJECT
        ],
        env=env_vars
    )

    # 3. Assert: Verify the CLI executed successfully
    if result.exit_code != 0:
        print(result.output)  # Print error output if test fails

    assert result.exit_code == 0
    assert "Ingest complete." in result.output

    # 4. Verification: Did we actually try to upload the file?
    # We inspect the calls made to our mock

    # Find the POST request to the objects endpoint
    upload_calls = [
        call for call in mock_gams_api.mock_calls
        if "POST" in str(call) and f"projects/{TEST_PROJECT}/objects" in str(call)
    ]

    assert len(upload_calls) == 1, "Expected exactly one upload POST request"

    # Inspect the arguments of that call to ensure the ZIP was attached
    _, _, kwargs = upload_calls[0]
    files = kwargs.get('files')

    assert 'subInfoPackZIP' in files
    # Check that we are sending a zip file (filename, content, mimetype)
    filename, file_content, mimetype = files['subInfoPackZIP']
    assert filename == "bag.zip"
    assert mimetype == "application/zip"
    # Even cooler: assert the zip is not empty (FileSystemService worked!)
    assert len(file_content) > 0
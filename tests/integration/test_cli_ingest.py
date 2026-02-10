
from click.testing import CliRunner
from pyrilo.cli import cli

def test_cli_ingest_flow_success(tmp_path, mock_pyrilo_ingest_env):
    """
    INTEGRATION TEST:
    1. Uses the pyrilo test data
    2. Runs the real 'pyrilo ingest' CLI command.
    3. Mocks only the network responses.

    Proofs:
    - CLI argument parsing works.
    - Authentication flow works.
    - FileSystem service correctly finds and zips files.
    - IngestService correctly constructs the API request.
    """

    gams_api_mock, test_pyrilo_project = mock_pyrilo_ingest_env

    # 1. Setup: Use already setup test bags
    bags_root = test_pyrilo_project.INGEST_BAGS_PATH

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
            "--host", test_pyrilo_project.TEST_HOST,
            "--bag_root", str(bags_root),  # points to the test data
            "--verbose",
            "ingest", test_pyrilo_project.TEST_PROJECT
        ],
        env=env_vars
    )

    # 3. Assert: Verify the CLI executed successfully
    if result.exit_code != 0:
        print(result.output)  # Print error output if test fails

    assert result.exit_code == 0
    assert "Ingest complete." in result.output

    # 4. Verification: Did we actually try to upload the file?
    # Use request_history to find the calls
    history = gams_api_mock.request_history

    # Filter for the ingest POST request
    upload_requests = [
        r for r in history
        if r.method == "POST" and f"projects/{test_pyrilo_project.TEST_PROJECT}/objects" in r.url
    ]

    assert len(upload_requests) == 1, "Expected exactly one upload POST request"

    # Verify the ZIP is in the body (Multipart verification is tricky with requests-mock,
    # but checking the header is a good start)
    last_request = upload_requests[0]
    assert "multipart/form-data" in last_request.headers.get("Content-Type", "")
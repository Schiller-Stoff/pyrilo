
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
            "--host", test_pyrilo_project.MOCK_HOST,
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
    # We inspect the calls made to our mock

    # Find the POST request to the objects endpoint
    upload_calls = [
        call for call in gams_api_mock.mock_calls
        if "POST" in str(call) and f"projects/{test_pyrilo_project.TEST_PROJECT}/objects" in str(call)
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
    # assert the zip is not empty (FileSystemService worked!)
    assert len(file_content) > 0
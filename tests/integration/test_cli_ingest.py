
from click.testing import CliRunner

# Import your actual entry point
from pyrilo.cli import cli
from utils.TestPyriloProject import TestPyriloProject


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
    bag_folder = bags_root / TestPyriloProject.TEST_BAG_NAME
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
            "--host", TestPyriloProject.MOCK_HOST,
            "--bag_root", str(bags_root),  # Point to our temp dir
            "--verbose",
            "ingest", TestPyriloProject.TEST_PROJECT
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
        if "POST" in str(call) and f"projects/{TestPyriloProject.TEST_PROJECT}/objects" in str(call)
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
from click.testing import CliRunner
from pyrilo.cli import cli

def test_cli_fails_gracefully_on_auth_error(mock_pyrilo_ingest_env):
    """
    Ensure the CLI exits with code 1 if login fails (401 Unauthorized).
    """
    gams_api_mock, test_pyrilo_project = mock_pyrilo_ingest_env

    # Override the login action to fail
    gams_api_mock.post("http://test-gams.local/login-action", status_code=401)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", test_pyrilo_project.MOCK_HOST,
        "create_project", test_pyrilo_project.TEST_PROJECT
    ], env={"PYRILO_USER": "wrong", "PYRILO_PASSWORD": "wrong"})

    # Should exit with 1 (system failure)
    assert result.exit_code == 1
    # Check that we logged the critical error (from cli.py)
    # "PermissionError" or "Login failed" depending on your AuthorizationService implementation
    assert "Initialization failed" in result.output or "Login failed" in result.output

def test_cli_fails_on_network_error(mock_pyrilo_ingest_env):
    """
    Ensure the CLI handles connection refused/timeout.
    """
    gams_api_mock, test_pyrilo_project = mock_pyrilo_ingest_env

    # Mock a connection exception for the auth endpoint
    import requests
    gams_api_mock.get("http://test-gams.local/api/v1/auth", exc=requests.exceptions.ConnectionError)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", test_pyrilo_project.TEST_PROJECT,
        "ingest", test_pyrilo_project.TEST_PROJECT
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 1
    assert "Network failure" in result.output
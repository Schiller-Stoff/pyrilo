from click.testing import CliRunner
from pyrilo.cli import cli

def test_cli_fails_gracefully_on_auth_error(mock_gams_api):
    """
    Ensure the CLI exits with code 1 if login fails (401 Unauthorized).
    """
    # Override the login action to fail
    mock_gams_api.post("http://test-gams.local/login-action", status_code=401)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", "http://test-gams.local",
        "create_project", "demo"
    ], env={"PYRILO_USER": "wrong", "PYRILO_PASSWORD": "wrong"})

    # Should exit with 1 (system failure)
    assert result.exit_code == 1
    # Check that we logged the critical error (from cli.py)
    # "PermissionError" or "Login failed" depending on your AuthorizationService implementation
    assert "Initialization failed" in result.output or "Login failed" in result.output

def test_cli_fails_on_network_error(mock_gams_api):
    """
    Ensure the CLI handles connection refused/timeout.
    """
    # Mock a connection exception for the auth endpoint
    import requests
    mock_gams_api.get("http://test-gams.local/api/v1/auth", exc=requests.exceptions.ConnectionError)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", "http://test-gams.local",
        "ingest", "demo"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 1
    assert "Network failure" in result.output
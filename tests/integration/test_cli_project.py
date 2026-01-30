from click.testing import CliRunner
from pyrilo.cli import cli


def test_create_project_success(mock_gams_api):
    """
    Verifies 'create_project' sends the correct PUT request with JSON body.
    """
    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", "http://test-gams.local",
        "create_project", "demo", "My Test Description"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 0
    assert "Successfully created project: demo" in result.output

    # Verify the API call details
    history = mock_gams_api.request_history
    put_requests = [r for r in history if r.method == "PUT" and r.url.endswith("/projects/demo")]

    assert len(put_requests) == 1
    assert put_requests[0].json()['description'] == "My Test Description"


def test_create_project_fails_if_exists(mock_gams_api):
    """
    Verifies correct error handling when GAMS returns 409 Conflict.
    """
    # Override the default 201 response with a 409 Conflict
    mock_gams_api.put("http://test-gams.local/api/v1/projects/demo", status_code=409)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", "http://test-gams.local",
        "create_project", "demo"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    # Expecting exit code 1 because cli.py catches Exception and calls sys.exit(1)
    assert result.exit_code == 1
    assert "Failed to create project" in result.output
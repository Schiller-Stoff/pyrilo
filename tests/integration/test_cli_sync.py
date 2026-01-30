from click.testing import CliRunner
from pyrilo.cli import cli
from utils.TestPyriloProject import TestPyriloProject


def test_sync_custom_search_integrate(mock_gams_api):
    """
    Test 'pyrilo sync custom_search <project>' triggers the specific POST endpoint.
    """
    # Register the specific custom search endpoint (since it's not in conftest generic regex)
    # Note: We use the exact URL we expect the code to hit
    target_url = f"{TestPyriloProject.MOCK_HOST}/api/v1/integration/c-search/projects/demo/objects"
    mock_gams_api.post(target_url, status_code=200)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", TestPyriloProject.MOCK_HOST,
        "sync", "custom_search", "demo"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 0

    # Verify we hit the specific integration endpoint
    history = mock_gams_api.request_history
    calls = [c for c in history if target_url in c.url and c.method == "POST"]
    assert len(calls) == 1


def test_sync_plexus_search_remove(mock_gams_api):
    """
    Test 'pyrilo sync plexus_search <project> --remove' triggers the DELETE endpoint.
    """
    target_url = f"{TestPyriloProject.MOCK_HOST}/api/v1/integration/plexus-search/projects/demo/objects"
    mock_gams_api.delete(target_url, status_code=200)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", TestPyriloProject.MOCK_HOST,
        "sync", "plexus_search", "demo", "--remove"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 0

    # Verify DELETE method
    history = mock_gams_api.request_history
    calls = [c for c in history if target_url in c.url and c.method == "DELETE"]
    assert len(calls) == 1
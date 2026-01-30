from click.testing import CliRunner
from pyrilo.cli import cli

def test_sync_custom_search_integrate(mock_pyrilo_ingest_env):
    """
    Test 'pyrilo sync custom_search <project>' triggers the specific POST endpoint.
    """
    gams_api_mock, test_pyrilo_project = mock_pyrilo_ingest_env

    # Register the specific custom search endpoint (since it's not in conftest generic regex)
    # Note: We use the exact URL we expect the code to hit
    target_url = f"{test_pyrilo_project.TEST_HOST}/api/v1/integration/c-search/projects/demo/objects"
    gams_api_mock.post(target_url, status_code=200)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", test_pyrilo_project.TEST_HOST,
        "sync", "custom_search", test_pyrilo_project.TEST_PROJECT
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 0

    # Verify we hit the specific integration endpoint
    history = gams_api_mock.request_history
    calls = [c for c in history if target_url in c.url and c.method == "POST"]
    assert len(calls) == 1


def test_sync_plexus_search_remove(mock_pyrilo_ingest_env):
    """
    Test 'pyrilo sync plexus_search <project> --remove' triggers the DELETE endpoint.
    """
    gams_api_mock, test_pyrilo_project = mock_pyrilo_ingest_env

    target_url = f"{test_pyrilo_project.TEST_HOST}/api/v1/integration/plexus-search/projects/demo/objects"
    gams_api_mock.delete(target_url, status_code=200)

    runner = CliRunner()
    result = runner.invoke(cli, [
        "--host", test_pyrilo_project.TEST_HOST,
        "sync", "plexus_search", test_pyrilo_project.TEST_PROJECT, "--remove"
    ], env={"PYRILO_USER": "u", "PYRILO_PASSWORD": "p"})

    assert result.exit_code == 0

    # Verify DELETE method
    history = gams_api_mock.request_history
    calls = [c for c in history if target_url in c.url and c.method == "DELETE"]
    assert len(calls) == 1
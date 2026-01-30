import pytest
import requests_mock
import re

from utils.TestPyriloProject import TestPyriloProject


@pytest.fixture
def mock_gams_api():
    """
    Patches the requests library using requests-mock with regex patterns.
    """
    with requests_mock.Mocker() as m:
        host = TestPyriloProject.MOCK_HOST
        api_base = f"{host}/api/v1"

        # ------------------------------------------------------------------
        # 1. Authentication Flow
        # ------------------------------------------------------------------
        m.get(
            f"{api_base}/auth",
            text='<form action="/login-action"><input type="hidden" name="execution" value="123"/></form>'
        )
        m.post(f"{host}/login-action", status_code=200, text="Login Successful")

        # ------------------------------------------------------------------
        # 2. Project Operations (The Missing Piece!)
        # ------------------------------------------------------------------
        # Matches: PUT .../projects/{ANY_PROJECT_ABBR}
        # We return 200 (or 201) to simulate successful creation
        project_pattern = re.compile(rf"{api_base}/projects/[^/]+$")
        m.put(project_pattern, status_code=201)

        # ------------------------------------------------------------------
        # 3. Digital Object Operations
        # ------------------------------------------------------------------

        # HEAD: Object Existence Check
        # Matches: .../projects/{project}/objects/{id}
        object_existence_pattern = re.compile(rf"{api_base}/projects/[^/]+/objects/[^/]+")
        m.head(object_existence_pattern, status_code=404)

        # POST: Ingest Object
        # Matches: .../projects/{project}/objects
        ingest_pattern = re.compile(rf"{api_base}/projects/[^/]+/objects$")
        m.post(ingest_pattern, status_code=201)

        yield m


@pytest.fixture
def test_pyrilo_ingest_files(tmp_path):
    return TestPyriloProject()


@pytest.fixture
def mock_pyrilo_ingest_env(mock_gams_api, test_pyrilo_ingest_files):
    return mock_gams_api, test_pyrilo_ingest_files
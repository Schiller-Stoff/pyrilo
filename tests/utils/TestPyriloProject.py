from pathlib import Path


class TestPyriloProject:
    """
    TODO description
    """

    # --- Test Data & Configuration ---
    TEST_PROJECT = "demo"
    TEST_BAG_NAME = f"{TEST_PROJECT}_bag_001" # TODO remove / update?
    MOCK_HOST = "http://test-gams.local"


    INGEST_BAGS_PATH =  Path(__file__).parent.parent / "resources" / "bags"
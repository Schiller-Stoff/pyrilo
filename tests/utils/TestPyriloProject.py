from pathlib import Path


class TestPyriloProject:
    """
    Wrapper for information about the test ingest files.
    """
    TEST_PROJECT = "demo"
    TEST_BAG_NAME = "memo.person.1"
    MOCK_HOST = "http://test-gams.local"
    INGEST_BAGS_PATH =  Path(__file__).parent.parent / "resources" / "bags"
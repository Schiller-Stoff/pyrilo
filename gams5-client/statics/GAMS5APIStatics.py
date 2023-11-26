
import os

class GAMS5APIStatics:
    """
    This class contains all statics for the GAMS5 API, like the API root path, the demo project abbreviation, the demo user name, etc.
    """

    API_ROOT = "/api/v1"
    DEMO_PROJECT_ABBR = "demo"
    DEMO_USER = "admin"

    # local paths for client to work
    LOCAL_PROJECT_FILES_PATH = os.getcwd() + "/project"
    LOCAL_SIP_FOLDERS_PATH = LOCAL_PROJECT_FILES_PATH + "/sips"
    LOCAL_BAGIT_FILES_PATH = LOCAL_PROJECT_FILES_PATH + "/bagit"

    def __init__(self) -> None:
        pass
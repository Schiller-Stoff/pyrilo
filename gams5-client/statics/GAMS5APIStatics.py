
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
    LOCAL_BAGIT_FILES_PATH = LOCAL_PROJECT_FILES_PATH + "/bags"
    # source file name of sips
    SIP_SOURCE_DATASTREAM_ID = "SOURCE"
    SIP_SOURCE_FILE_NAME = SIP_SOURCE_DATASTREAM_ID + ".xml"
    # Thumbnail
    THUMBNAIL_DATASTREAM_ID = "THUMBNAIL"
    THUMBNAIL_FILE_NAME = THUMBNAIL_DATASTREAM_ID + ".jpg"
    THUMBNAIL_SIP_SOURCE_FILE_NAME = "1.JPG"
    # search json
    SIP_SEARCH_JSON_DATASTREAM_ID = "SEARCH_INDEX"
    SIP_SEARCH_JSON_FILE_NAME = SIP_SEARCH_JSON_DATASTREAM_ID + ".json"

    def __init__(self) -> None:
        pass
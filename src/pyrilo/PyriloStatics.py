
import os
import pathlib

class PyriloStatics:
    """
    This class contains all statics for the GAMS5 API, like the API root path, the demo project abbreviation, the demo user name, etc.
    all paths are relative to the current working directory.
    """

    API_ROOT = "/api/v1"
    AUTH_ENDPOINT = API_ROOT + "/auth"
    DEMO_PROJECT_ABBR = "demo"
    DEMO_USER = "admin"

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
    # integration api statics, e.g. type of digital object
    # type field category for digital object type
    INTEGRATION_API_OBJECT_TYPE = "digitalObject"

    def __init__(self) -> None:
        pass
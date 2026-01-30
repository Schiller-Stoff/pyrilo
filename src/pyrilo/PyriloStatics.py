class PyriloStatics:
    """
    This class contains all statics for the GAMS5 API, like the API root path, the demo project abbreviation, the demo user name, etc.
    all paths are relative to the current working directory.
    """

    API_ROOT = "/api/v1"
    AUTH_ENDPOINT = API_ROOT + "/auth"

    def __init__(self) -> None:
        pass
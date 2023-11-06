
from enums.GAMS5APIStatics import GAMS5APIStatics


class DigitalObjectService:
    """
    Service class for operations on digital objects.
    """

    ## TODO class needs configuration - what is the hostname / port to request against?


    def __init__(self) -> None:
        pass


    def create_object(id: str, project_abbr: str):
        """
        Creates given digital object for project.

        """
        # TODO implement

        create_object_path = f"{GAMS5APIStatics.API_ROOT}/projects/{project_abbr}/objects/{id}"


    def list_objects(project_abbr: str):
        """
        Retrieves an overview over all digital objects for given project.
        """

        # TODO implement - return a list of digital objects (domain class) to work on. 





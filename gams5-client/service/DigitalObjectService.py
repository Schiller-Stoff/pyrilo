
from statics.GAMS5APIStatics import GAMS5APIStatics
from domain.DigitalObject import DigitalObject
from typing import Dict
import requests
import json

class DigitalObjectService:
    """
    Service class for operations on digital objects.
    """

    ## TODO class needs configuration - what is the hostname / port to request against?
    auth: Dict[str, str] | None

    # TODO also need the hostname (with protocol and port!)
    host: str

    # do some error control? (should not contain trailing slashes etc.) 
    API_BASE_PATH: str

    def __init__(self, host: str) -> None:
        self.host = host
        self.API_BASE_PATH = f"{host}{GAMS5APIStatics.API_ROOT}"
        pass


    def create_object(self, id: str, project_abbr: str):
        """
        Creates given digital object for project.

        """
        # TODO implement

        create_object_path = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"


    def list_objects(self, project_abbr: str):
        """
        Retrieves an overview over all digital objects for given project.
        """

        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects"
        response = requests.get(url)

        response_object_list = response.json()

        digital_objects = []
        for response_object in response_object_list:
            # TODO mapping from api-response to digital object is error prone here
            digital_objects.append(
                DigitalObject(response_object["id"], project_abbr, response_object["datastreams"])
            )

        return digital_objects





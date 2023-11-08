from service.DigitalObjectService import DigitalObjectService
from typing import List
import logging
import os

class GAMS5APIClient:
    """
    Provides abstractions for the usage of the gams5-api, like:
    - creating digital objects
    - requesting lists of datastreams for a digital object etc.
    """

    digital_object_service: DigitalObjectService

    def __init__(self, host: str) -> None:
        self.digital_object_service = DigitalObjectService(host)

    def configure_auth(self, user_name: str, user_pw: str):
        """
        Configures authentication for state changing operations via the REST-API.
        """
        self.digital_object_service.auth = (user_name, user_pw)

    def list_objects(self, project_abbr: str) -> List[str]:
        """
        Lists all objects of defined project
        """

        return self.digital_object_service.list_objects(project_abbr)
    
    def save_object(self, id: str, project_abbr: str):
        """
        Creates a digital object 
        """
        return self.digital_object_service.save_object(id, project_abbr)
    
    def ingest():
        """
        Ingests defined folder / package structure.
        """
        # TODO implement ...

    
    
from service.SubInfoPackService import SubInfoPackService
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
    sub_info_pack_service: SubInfoPackService

    def __init__(self, host: str) -> None:
        self.digital_object_service = DigitalObjectService(host)
        self.sub_info_pack_service = SubInfoPackService(host)

    def configure_auth(self, user_name: str, user_pw: str):
        """
        Configures authentication for state changing operations via the REST-API.
        """
        self.digital_object_service.auth = (user_name, user_pw)
        self.sub_info_pack_service.auth = (user_name, user_pw)

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
    
    def ingest_sip(self, project_abbr: str, sip_folder_name: str):
        """
        Ingests defined folder from the local SIP structure.
        """
        self.sub_info_pack_service.ingest_folder_object(project_abbr, sip_folder_name)


    def ingest(self, project_abbr: str):
        """
        Walks through project directory and ingests individual objects.
        """
        # TODO loop through directory and call method 
        # self.sub_info_pack_service.ingest_folder_object(project_abbr, "demo1")
        raise NotImplementedError("Not implemented!")

    
    
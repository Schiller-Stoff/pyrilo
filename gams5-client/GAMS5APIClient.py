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

        
if __name__ == "__main__":

    log_file_path = f"{os.getcwd()}/logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    # example usage of the client
    MY_PROJECT = "demo"
    # TODO configuring - maybe for handling auth thats not a good idea? e.g. GET requesting should possible all the time VS state changing operations
    # need to throw an error. --> maybe own configure_auth() method?
    client = GAMS5APIClient("http://localhost:18085")
    # configure authentication ins separate method.
    client.configure_auth("admin", "admin")

    found_objects = client.list_objects(MY_PROJECT)
    print(found_objects) 

    client.save_object("demo4", MY_PROJECT)

    
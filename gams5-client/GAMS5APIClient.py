from service.DigitalObjectService import DigitalObjectService
from typing import List

class GAMS5APIClient:
    """
    Provides abstractions for the usage of the gams5-api, like:
    - creating digital objects
    - requesting lists of datastreams for a digital object etc.
    """

    host: str
    user_name: str
    user_pw: str

    def __init__(self, host: str) -> None:
        self.host = host

    def configure_auth(self, user_name: str, user_pw: str):
        """
        Configures authentication for state changing operations via the REST-API.
        """
        self.user_name = user_name
        self.user_pw = user_pw

    
    def list_objects(self, project_abbr: str) -> List[str]:
        """
        Lists all objects of defined project
        """

        return DigitalObjectService.list_objects(project_abbr)
        

if __name__ == "__main__":

    # example usage of the client
    MY_PROJECT = "demo"
    # TODO configuring - maybe for handling auth thats not a good idea? e.g. GET requesting should possible all the time VS state changing operations
    # need to throw an error. --> maybe own configure_auth() method?
    client = GAMS5APIClient("http://locahlhost:18085")
    # configure authentication ins separate method.
    client.configure_auth("admin", "admin")

    found_objects = client.list_objects(MY_PROJECT)
    print(found_objects)
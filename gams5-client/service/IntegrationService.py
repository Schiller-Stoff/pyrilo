from statics.GAMS5APIStatics import GAMS5APIStatics
from urllib3 import make_headers, request
import logging

class IntegrationService:
    """
    Handles operations on GAMS integration endpoints, like triggering indexation to 
    certain databases etc.
    """

    auth: tuple | None = None
    host: str
    # do some error control? (should not contain trailing slashes etc.) 
    API_BASE_PATH: str

    def __init__(self, host: str, auth: tuple | None = None) -> None:
        self.host = host
        self.auth = auth
        self.API_BASE_PATH = f"{host}{GAMS5APIStatics.API_ROOT}"

    
    def integrate_all(self, project_abbr: str):
        """
        Integrate all digital objects of a project to gams-integration services.
        """
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects"
        r = request("POST", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False, timeout=300)

        if r.status >= 400:
            msg = f"Failed to integrate all objects for project {project_abbr}. POST request against {url}. Status: {r.status}. Response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated all digital objects for project {project_abbr}.")


    def disintegrate_all(self, project_abbr: str):
        """
        Disintegrate all digital objects of a project from gams-integration services.
        """
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects"
        r = request("DELETE", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False, timeout=30)

        if r.status >= 400:
            msg = f"Failed to disintegrate all objects for project {project_abbr}. POST request against {url}. Status: {r.status}."
            logging.error(msg)
            logging.error(f"Response: {r.json()}")
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated all digital objects for project {project_abbr}.")


    def integrate(self, project_abbr: str, object_id: str):
        """
        Creates database entries for a singular digital object of a project in gams-integration services.
        """
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/{object_id}"
        r = request("POST", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False, timeout=30)

        if r.status >= 400:
            msg = f"Failed to integrate object {object_id} for project {project_abbr}. POST request against {url}. Status: {r.status}. Response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated object {object_id} for project {project_abbr}.")


    def disintegrate(self, project_abbr: str, object_id: str):
        """
        Disintegrate (=removes database entries) a single digital object of a project from gams-integration services.
        """
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/{object_id}"
        r = request("DELETE", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False, timeout=30)

        if r.status >= 400:
            msg = f"Failed to disintegrate object {object_id} for project {project_abbr}. DELETE request against {url}. Status: {r.status}. Response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated object {object_id} for project {project_abbr}.")
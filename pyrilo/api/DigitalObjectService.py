
import logging
from PyriloStatics import PyriloStatics
from api.DigitalObject import DigitalObject
from typing import Dict, List
from urllib3 import make_headers, request, encode_multipart_formdata

class DigitalObjectService:
    """
    Service class for operations on digital objects.
    """
    # tuple for basic auth - 1. user_name 2. user_password
    auth: tuple | None = None
    host: str
    # do some error control? (should not contain trailing slashes etc.) 
    API_BASE_PATH: str

    def __init__(self, host: str, auth: tuple | None = None) -> None:
        self.host = host
        self.auth = auth
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def save_object(self, id: str, project_abbr: str):
        """
        Creates digital object for project with given id.

        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"
        r = request("PUT", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created digital object with id {id} for project {project_abbr}.")



    def list_objects(self, project_abbr: str):
        """
        Retrieves an overview over all digital objects for given project.

        """

        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects"
        r = request("GET", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully retrieved digital objects for project {project_abbr}.")
        
        response_object_list = r.json()

        digital_objects = []
        for response_object in response_object_list:
            # TODO mapping from api-response to digital object is error prone here
            digital_objects.append(
                DigitalObject(response_object["id"], project_abbr, response_object["datastreams"])
            )

        return digital_objects


    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns child objects to a parent object. Sends the correspondnet request to the gams-api.
        :param parent_id: id of the parent object
        :param children_ids: list of ids of child objects 
        """
        # enpoint allowing to create child parent relationships.
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{parent_id}/collect"

        # construct headers
        headers = make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}')
        child_ids_string = ",".join(children_ids)
        body_form_data, content_type = encode_multipart_formdata({"childObjects": child_ids_string}, boundary=None)
        headers["Content-Type"] = content_type

        # construct a multipart request via formdata
        r = request("PATCH", url, headers=headers, redirect=False, body=body_form_data)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully assigned child-objects to object {parent_id} for project {project_abbr}.")



    def delete_object(self, id: str, project_abbr: str):
        """
        Deletes a digital object with given id.

        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"
        r = request("DELETE", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False)

        if r.status >= 400:
            msg = f"Failed to delete object {id} for project {project_abbr}. DELETE request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted digital object with id {id}.")

    def delete_objects(self, project_abbr: str):
        """
        Deletes all digital objects for given project.

        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects"
        r = request("DELETE", url, headers= make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}') if self.auth else None, redirect=False, timeout=10)

        if r.status >= 400:
            msg = f"Failed to DELETE all objects for project {project_abbr}. DELETE request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted all digital objects for project {project_abbr}.")
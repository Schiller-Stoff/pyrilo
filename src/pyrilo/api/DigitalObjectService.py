
import logging
from pyrilo.PyriloStatics import PyriloStatics
from typing import List, Dict, Any
from urllib3 import request, encode_multipart_formdata

from pyrilo.api.auth.AuthCookie import AuthCookie


class DigitalObjectService:
    """
    Service class for operations on digital objects.
    """
    # tuple for basic auth - 1. user_name 2. user_password
    auth: AuthCookie | None
    host: str
    # do some error control? (should not contain trailing slashes etc.) 
    API_BASE_PATH: str

    def __init__(self, host: str, auth: AuthCookie | None = None) -> None:
        self.host = host
        self.auth = auth
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def object_exists(self, id: str, project_abbr: str):
        """
        Checks if a digital object exists on the gams-api.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"
        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("HEAD", url, headers=headers, redirect=False)

        if r.status >= 400:
            return False
        else:
            logging.debug(f"Successfully requested digital objects for project {project_abbr}.")
            return True

    def save_object(self, id: str, project_abbr: str):
        """
        Creates digital object for project with given id.

        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("PUT", url, headers=headers, redirect=False)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created digital object with id {id} for project {project_abbr}.")



    def list_objects(self, project_abbr: str, object_ids: None | List[str] = None, page_index: int = 0):
        """
        Retrieves an overview over all digital objects for given project.

        """
        # needed for recursion
        if object_ids is None:
            object_ids: List[str] = []
        else:
            # if a list of objects was already retrieved -> increment pageIndex
            page_index += 1


        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/ids?pageIndex={str(page_index)}"
        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("GET", url, headers=headers)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.debug(f"Successfully GET requested digital objects for project {project_abbr}.")

        # paginated object ids
        paginated_response_object: Dict[str, Any] = r.json()
        paginated_id_list = paginated_response_object.get("results")

        # digital_object_ids: List[str] = []
        for object_id in paginated_id_list:
            object_ids.append(object_id)

        # if pagination.hasNext = true
        if paginated_response_object.get("pagination").get("hasNext") is True:
            logging.debug("hasNext property in returned pagination is true -> calling now the method recursively to aggregate all digital objects")
            return self.list_objects(project_abbr, object_ids, page_index)
        else:
            logging.info(f"Successfully retrieved digital objects for project {project_abbr}.")
            return object_ids


    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns child objects to a parent object. Sends the correspondnet request to the gams-api.
        :param parent_id: id of the parent object
        :param children_ids: list of ids of child objects 
        """
        # enpoint allowing to create child parent relationships.
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{parent_id}/collect"

        # construct headers
        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
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
        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("DELETE", url, headers=headers, redirect=False)

        if r.status >= 400:
            msg = f"Failed to delete object {id} for project {project_abbr}. DELETE request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted digital object with id {id}.")

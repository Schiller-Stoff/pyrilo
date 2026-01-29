import logging
from pyrilo.PyriloStatics import PyriloStatics
from typing import List, Dict, Any
import requests


class DigitalObjectService:
    """
    Service class for operations on digital objects using requests.Session.
    """
    session: requests.Session
    host: str
    API_BASE_PATH: str

    def __init__(self, session: requests.Session, host: str) -> None:
        self.host = host
        self.session = session
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def object_exists(self, id: str, project_abbr: str):
        """
        Checks if a digital object exists on the gams-api.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"

        # Requests handles cookies automatically via the session
        r = self.session.head(url)

        if r.status_code >= 400:
            return False
        else:
            logging.debug(f"Successfully requested digital objects for project {project_abbr}.")
            return True

    def save_object(self, id: str, project_abbr: str):
        """
        Creates digital object for project with given id.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"

        r = self.session.put(url)

        if r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created digital object with id {id} for project {project_abbr}.")

    def list_objects(self, project_abbr: str, object_ids: None | List[str] = None, page_index: int = 0):
        """
        Retrieves an overview over all digital objects for given project.
        """
        if object_ids is None:
            object_ids: List[str] = []
        else:
            page_index += 1

        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/ids"
        params = {"pageIndex": str(page_index)}

        r = self.session.get(url, params=params)

        if r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.debug(f"Successfully GET requested digital objects for project {project_abbr}.")

        paginated_response_object: Dict[str, Any] = r.json()
        paginated_id_list = paginated_response_object.get("results")

        for object_id in paginated_id_list:
            object_ids.append(object_id)

        if paginated_response_object.get("pagination").get("hasNext") is True:
            logging.debug("hasNext property in returned pagination is true -> recursing")
            return self.list_objects(project_abbr, object_ids, page_index)
        else:
            logging.info(f"Successfully retrieved digital objects for project {project_abbr}.")
            return object_ids

    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns child objects to a parent object.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{parent_id}/collect"

        child_ids_string = ",".join(children_ids)
        # Requests automatically sets boundary for files/multipart, but here we are sending fields
        data = {"childObjects": child_ids_string}

        r = self.session.patch(url, data=data)

        if r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully assigned child-objects to object {parent_id} for project {project_abbr}.")

    def delete_object(self, id: str, project_abbr: str):
        """
        Deletes a digital object with given id.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/{id}"

        r = self.session.delete(url)

        if r.status_code >= 400:
            msg = f"Failed to delete object {id} for project {project_abbr}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
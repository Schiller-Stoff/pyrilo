import logging
from typing import List, Dict, Any, Optional
from pyrilo.api.GamsApiClient import GamsApiClient


class DigitalObjectService:
    """
    Service class for operations on digital objects using GamsApiClient.
    """
    client: GamsApiClient

    def __init__(self, client: GamsApiClient) -> None:
        self.client = client

    def object_exists(self, id: str, project_abbr: str) -> bool:
        """
        Checks if a digital object exists on the gams-api.
        """
        # We disable auto-error raising because a 404 simply means "False" here,
        # not a system failure.
        r = self.client.head(
            f"projects/{project_abbr}/objects/{id}",
            raise_errors=False
        )

        if r.status_code >= 400:
            return False
        else:
            logging.debug(f"Successfully requested digital objects for project {project_abbr}.")
            return True

    def save_object(self, id: str, project_abbr: str):
        """
        Creates digital object for project with given id.
        """
        self.client.put(f"projects/{project_abbr}/objects/{id}")
        logging.info(f"Successfully created digital object with id {id} for project {project_abbr}.")

    def list_objects(self, project_abbr: str, object_ids: Optional[List[str]] = None, page_index: int = 0):
        """
        Retrieves an overview over all digital objects for given project.
        """
        if object_ids is None:
            object_ids = []
        else:
            page_index += 1

        params = {"pageIndex": str(page_index)}

        # The client handles the URL and error checking (>= 400) automatically
        r = self.client.get(
            f"projects/{project_abbr}/objects/ids",
            params=params
        )

        logging.debug(f"Successfully GET requested digital objects for project {project_abbr}.")

        paginated_response_object: Dict[str, Any] = r.json()
        paginated_id_list = paginated_response_object.get("results", [])

        # Append current page results
        object_ids.extend(paginated_id_list)

        # Check for recursion
        if paginated_response_object.get("pagination", {}).get("hasNext") is True:
            logging.debug("hasNext property in returned pagination is true -> recursing")
            return self.list_objects(project_abbr, object_ids, page_index)
        else:
            logging.info(f"Successfully retrieved digital objects for project {project_abbr}.")
            return object_ids

    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns child objects to a parent object.
        """
        child_ids_string = ",".join(children_ids)
        # We pass data (form fields) just like in standard requests
        data = {"childObjects": child_ids_string}

        self.client.patch(
            f"projects/{project_abbr}/objects/{parent_id}/collect",
            data=data
        )

        logging.info(f"Successfully assigned child-objects to object {parent_id} for project {project_abbr}.")

    def delete_object(self, id: str, project_abbr: str):
        """
        Deletes a digital object with given id.
        """
        self.client.delete(f"projects/{project_abbr}/objects/{id}")
        logging.info(f"Successfully deleted object {id} for project {project_abbr}.")
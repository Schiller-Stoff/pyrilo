import logging
from pyrilo.api.auth.AuthCookie import AuthCookie
from pyrilo.PyriloStatics import PyriloStatics
from urllib3 import request

class CollectionService:
    """
    TODO
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

    def delete_collection(self, project_abbr: str, collection_id: str):
        """
        Deletes specified GAMS collection of digital objects
        :param project_abbr owning project of the GAMS-collection
        :param collection_id id of the collection to be saved
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/collections/{collection_id}"

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("DELETE", url, headers=headers, redirect=False)

        if r.status == 404:
            msg = f"Collection with id {collection_id} for project {project_abbr} does not exist!"
            logging.info(msg)
            raise ValueError(msg)
        elif r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted collection with id {collection_id} for project {project_abbr}.")



    def save_collection(self, project_abbr: str, collection_id: str, title: str, desc: str):
        """
        Saves a GAMS collection via the GAMS.API
        :param project_abbr owning project of the GAMS-collection
        :param collection_id id of the collection to be saved
        :param title or label of the collection.
        :param desc description of the collection.
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/collections/{collection_id}"

        request_body = {
            "id": collection_id,
            "project": {
                "projectAbbr": project_abbr
            },
            "title": title,
            "description": desc
        }

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("PUT", url, headers=headers, json=request_body, redirect=False)

        if r.status == 409:
            msg = f"Collection with id {collection_id} for project already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status == 403:
            msg = f"User is not authorized to create the collection '{collection_id}'. Only the gams admin may create / delete projects."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created collection with id {collection_id} for project {project_abbr}.")
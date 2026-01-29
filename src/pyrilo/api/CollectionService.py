import logging
from pyrilo.PyriloStatics import PyriloStatics
import requests


class CollectionService:
    session: requests.Session
    host: str
    API_BASE_PATH: str

    def __init__(self, session: requests.Session, host: str) -> None:
        self.host = host
        self.session = session
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def delete_collection(self, project_abbr: str, collection_id: str):
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/collections/{collection_id}"

        r = self.session.delete(url)

        if r.status_code == 404:
            msg = f"Collection with id {collection_id} for project {project_abbr} does not exist!"
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted collection {collection_id} for project {project_abbr}.")

    def save_collection(self, project_abbr: str, collection_id: str, title: str, desc: str):
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}/collections/{collection_id}"

        request_body = {
            "id": collection_id,
            "project": {
                "projectAbbr": project_abbr
            },
            "title": title,
            "description": desc
        }

        r = self.session.put(url, json=request_body)

        if r.status_code == 409:
            msg = f"Collection with id {collection_id} already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code == 403:
            msg = f"User is not authorized to create the collection '{collection_id}'."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created collection {collection_id} for project {project_abbr}.")
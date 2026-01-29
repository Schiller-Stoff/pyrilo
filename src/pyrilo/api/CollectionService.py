import logging
from pyrilo.api.GamsApiClient import GamsApiClient


class CollectionService:
    client: GamsApiClient

    def __init__(self, client: GamsApiClient) -> None:
        self.client = client

    def delete_collection(self, project_abbr: str, collection_id: str):
        # We disable auto-raising errors because we want to handle 404 specifically
        r = self.client.delete(
            f"projects/{project_abbr}/collections/{collection_id}",
            raise_errors=False
        )

        if r.status_code == 404:
            msg = f"Collection with id {collection_id} for project {project_abbr} does not exist!"
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to delete collection {collection_id}. Status: {r.status_code}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted collection {collection_id} for project {project_abbr}.")

    def save_collection(self, project_abbr: str, collection_id: str, title: str, desc: str):
        request_body = {
            "id": collection_id,
            "project": {
                "projectAbbr": project_abbr
            },
            "title": title,
            "description": desc
        }

        r = self.client.put(
            f"projects/{project_abbr}/collections/{collection_id}",
            json=request_body,
            raise_errors=False
        )

        if r.status_code == 409:
            msg = f"Collection with id {collection_id} already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code == 403:
            msg = f"User is not authorized to create the collection '{collection_id}'."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to create collection. Status: {r.status_code}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created collection {collection_id} for project {project_abbr}.")
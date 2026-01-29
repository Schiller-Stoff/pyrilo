import logging
from pyrilo.api.GamsApiClient import GamsApiClient


class ProjectService:
    client: GamsApiClient

    def __init__(self, client: GamsApiClient) -> None:
        self.client = client

    def save_project(self, project_abbr: str, description: str):
        r = self.client.put(
            f"projects/{project_abbr}",
            json={"description": description},
            raise_errors=False
        )

        if r.status_code == 409:
            msg = f"Project with abbreviation {project_abbr} already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code == 403:
            msg = f"User is not authorized to create the project '{project_abbr}'."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to save project. Status: {r.status_code}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created project with abbreviation {project_abbr}.")

    def update_project(self, project_abbr: str, description: str):
        r = self.client.patch(
            f"projects/{project_abbr}",
            json={"description": description},
            raise_errors=False
        )

        if r.status_code == 403:
            msg = f"User is not authorized to update the project '{project_abbr}'."
            logging.error(msg)
            raise PermissionError(msg)
        if r.status_code == 404:
            msg = f"Requested project {project_abbr} to be updated does not exist!"
            logging.error(msg)
            raise ValueError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to update project. Status: {r.status_code}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully updated project with abbreviation {project_abbr}.")

    def delete_project(self, project_abbr: str):
        # Default error handling is sufficient here (>= 400 raises ConnectionError)
        self.client.delete(f"projects/{project_abbr}")
        logging.info(f"Successfully deleted project with abbreviation {project_abbr}.")

    def trigger_project_integration(self, project_abbr: str):
        self.client.post(f"integration/projects/{project_abbr}/objects/search/setup")
        logging.info(f"Successfully created project integration for {project_abbr}.")
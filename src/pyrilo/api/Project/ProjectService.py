import logging
from pyrilo.api.GamsApiClient import GamsApiClient
from pyrilo.api.Project.exceptions import ProjectAlreadyExistsError
from pyrilo.exceptions import PyriloPermissionError, PyriloApiError, PyriloConflictError


class ProjectService:
    client: GamsApiClient

    def __init__(self, client: GamsApiClient) -> None:
        self.client = client

    def save_project(self, project_abbr: str, description: str):
        try:
            self.client.put(
                f"projects/{project_abbr}",
                json={"description": description}
                # remove raise_errors=False if you want the client to handle it automatically
                # or keep it False and manually check status like below:
            )
        except PyriloConflictError:
            # You can re-raise with a better message, or let the client error bubble up
            msg = f"Project with abbreviation {project_abbr} already exists."
            raise ProjectAlreadyExistsError(msg)

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
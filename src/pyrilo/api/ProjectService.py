import logging
from pyrilo.PyriloStatics import PyriloStatics
import requests


class ProjectService:
    """
    Handles requests against the GAMS5 API for projects using requests.Session.
    """
    session: requests.Session
    host: str
    API_BASE_PATH: str

    def __init__(self, session: requests.Session, host: str) -> None:
        self.host = host
        self.session = session
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def save_project(self, project_abbr: str, description: str):
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}"

        r = self.session.put(url, json={"description": description})

        if r.status_code == 409:
            msg = f"Project with abbreviation {project_abbr} already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status_code == 403:
            msg = f"User is not authorized to create the project '{project_abbr}'."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created project with abbreviation {project_abbr}.")

    def update_project(self, project_abbr: str, description: str):
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}"

        r = self.session.patch(url, json={"description": description})

        if r.status_code == 403:
            msg = f"User is not authorized to update the project '{project_abbr}'."
            logging.error(msg)
            raise PermissionError(msg)
        if r.status_code == 404:
            msg = f"Requested project {project_abbr} to be updated does not exist!"
            logging.error(msg)
            raise ValueError(msg)
        elif r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully updated project with abbreviation {project_abbr}.")

    def delete_project(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}"

        r = self.session.delete(url)

        if r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully deleted project with abbreviation {project_abbr}.")

    def trigger_project_integration(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/search/setup"

        r = self.session.post(url)

        if r.status_code >= 400:
            msg = f"Failed to request against {url}. API response: {r.text}"
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created project integration for {project_abbr}.")
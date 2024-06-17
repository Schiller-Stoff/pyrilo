import logging
from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.api.auth.AuthCookie import AuthCookie
from urllib3 import request

class ProjectService:
    """
    Handles requests against the GAMS5 API for projects.
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

    def save_project(self, project_abbr: str, description: str):
        """
        Creates a new project with given abbreviation and description.
        :param project_abbr: abbreviation of the project
        :param description: description of the project
        :raises ValueError: if project with abbreviation already exists
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}"

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("PUT", url, headers=headers, json={"description": description}, redirect=False)

        if r.status == 409:
            msg = f"Project with abbreviation {project_abbr} already exists."
            logging.info(msg)
            raise ValueError(msg)
        elif r.status == 403:
            msg = f"User is not authorized to create the project '{project_abbr}'."
            logging.error(msg)
            raise PermissionError(msg)
        elif r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created project with abbreviation {project_abbr}.")


    def delete_project(self, project_abbr: str):
        """
        Deletes a project.
        :param project_abbr: abbreviation of the project
        """
        url = f"{self.API_BASE_PATH}/projects/{project_abbr}"

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("DELETE", url, headers=headers, redirect=False)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully created project with abbreviation {project_abbr}.")



    def trigger_project_integration(self, project_abbr: str):
        """
        Triggers the integration of a project.
        """
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/search/setup"

        # use cookie header if available
        headers = self.auth.build_auth_cookie_header() if self.auth else None
        r = request("POST", url, headers=headers, redirect=False)

        if r.status >= 400:
            # TODO err msg
            msg = f"Failed to request against {url}. API response: {r.json()}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            # TODO msg
            logging.info(f"Successfully created project integration for porject with abbreviation {project_abbr}.")
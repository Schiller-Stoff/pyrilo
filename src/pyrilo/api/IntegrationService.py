from pyrilo.PyriloStatics import PyriloStatics
import requests
import logging

class IntegrationService:
    """
    Handles operations on GAMS integration endpoints using requests.Session.
    """
    session: requests.Session
    host: str
    API_BASE_PATH: str

    def __init__(self, session: requests.Session, host: str) -> None:
        self.host = host
        self.session = session
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    def integrate_all(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects"
        r = self.session.post(url, timeout=300)

        if r.status_code >= 400:
            msg = f"Failed to integrate all objects for project {project_abbr}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated all digital objects for project {project_abbr}.")

    def disintegrate_all(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects"
        r = self.session.delete(url, timeout=30)

        if r.status_code >= 400:
            msg = f"Failed to disintegrate all objects for project {project_abbr}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated all digital objects for project {project_abbr}.")

    def integrate_all_custom_search(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/c-search/projects/{project_abbr}/objects"
        r = self.session.post(url, timeout=300)

        if r.status_code >= 400:
            msg = f"Failed to integrate all objects to customSearch. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated all objects to customSearch for project {project_abbr}.")

    def disintegrate_all_custom_search(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/c-search/projects/{project_abbr}/objects"
        r = self.session.delete(url, timeout=30)

        if r.status_code >= 400:
            msg = f"Failed to disintegrate all objects from customSearch. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated all objects from customSearch for project {project_abbr}.")

    def integrate_all_plexus_search(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/plexus-search/projects/{project_abbr}/objects"
        r = self.session.post(url, timeout=300)

        if r.status_code >= 400:
            msg = f"Failed to integrate all objects to plexusSearch. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated all objects to plexusSearch for project {project_abbr}.")

    def disintegrate_all_plexus_search(self, project_abbr: str):
        url = f"{self.API_BASE_PATH}/integration/plexus-search/projects/{project_abbr}/objects"
        r = self.session.delete(url, timeout=30)

        if r.status_code >= 400:
            msg = f"Failed to disintegrate all objects from plexusSearch. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated all objects from plexusSearch for project {project_abbr}.")

    def integrate(self, project_abbr: str, object_id: str):
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/{object_id}"
        r = self.session.post(url, timeout=30)

        if r.status_code >= 400:
            msg = f"Failed to integrate object {object_id}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully integrated object {object_id} for project {project_abbr}.")

    def disintegrate(self, project_abbr: str, object_id: str):
        url = f"{self.API_BASE_PATH}/integration/projects/{project_abbr}/objects/{object_id}"
        r = self.session.delete(url, timeout=30)

        if r.status_code >= 400:
            msg = f"Failed to disintegrate object {object_id}. Response: {r.text}"
            logging.error(msg)
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully disintegrated object {object_id} for project {project_abbr}.")
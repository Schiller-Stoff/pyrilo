import logging
from pyrilo.api.GamsApiClient import GamsApiClient


class IntegrationService:
    client: GamsApiClient

    def __init__(self, client: GamsApiClient) -> None:
        self.client = client

    def integrate_all(self, project_abbr: str):
        self.client.post(
            f"integration/projects/{project_abbr}/objects",
            timeout=300
        )
        logging.info(f"Successfully integrated all digital objects for project {project_abbr}.")

    def disintegrate_all(self, project_abbr: str):
        self.client.delete(
            f"integration/projects/{project_abbr}/objects",
            timeout=30
        )
        logging.info(f"Successfully disintegrated all digital objects for project {project_abbr}.")

    def integrate_all_custom_search(self, project_abbr: str):
        self.client.post(
            f"integration/c-search/projects/{project_abbr}/objects",
            timeout=300
        )
        logging.info(f"Successfully integrated all objects to customSearch for project {project_abbr}.")

    def disintegrate_all_custom_search(self, project_abbr: str):
        self.client.delete(
            f"integration/c-search/projects/{project_abbr}/objects",
            timeout=30
        )
        logging.info(f"Successfully disintegrated all objects from customSearch for project {project_abbr}.")

    def integrate_all_plexus_search(self, project_abbr: str):
        self.client.post(
            f"integration/plexus-search/projects/{project_abbr}/objects",
            timeout=300
        )
        logging.info(f"Successfully integrated all objects to plexusSearch for project {project_abbr}.")

    def disintegrate_all_plexus_search(self, project_abbr: str):
        self.client.delete(
            f"integration/plexus-search/projects/{project_abbr}/objects",
            timeout=30
        )
        logging.info(f"Successfully disintegrated all objects from plexusSearch for project {project_abbr}.")

    def integrate(self, project_abbr: str, object_id: str):
        self.client.post(
            f"integration/projects/{project_abbr}/objects/{object_id}",
            timeout=30
        )
        logging.info(f"Successfully integrated object {object_id} for project {project_abbr}.")

    def disintegrate(self, project_abbr: str, object_id: str):
        self.client.delete(
            f"integration/projects/{project_abbr}/objects/{object_id}",
            timeout=30
        )
        logging.info(f"Successfully disintegrated object {object_id} for project {project_abbr}.")
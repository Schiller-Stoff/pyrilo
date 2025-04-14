import logging

from pyrilo.PyriloStatics import PyriloStatics
from pyrilo.api.CollectionService import CollectionService
from pyrilo.api.DigitalObjectService import DigitalObjectService
from pyrilo.api.IngestService import IngestService
from pyrilo.api.IntegrationService import IntegrationService
from typing import List
from pyrilo.api.ProjectService import ProjectService
from pyrilo.api.auth.AuthorizationService import AuthorizationService


class Pyrilo:
    """
    Provides abstractions for the usage of GAMS5 REST-API, like:
    - ingesting SIPs as digital objects and datastreams
    - check method names for more
    """

    digital_object_service: DigitalObjectService
    ingest_service: IngestService
    integration_service: IntegrationService
    authorization_service: AuthorizationService
    project_service: ProjectService
    collection_service: CollectionService
    host: str

    def __init__(self, host: str) -> None:
        self.configure(host)

    def configure(self, host: str, local_bagit_files_path: str = PyriloStatics.LOCAL_BAGIT_FILES_PATH):
        """
        Configures the Pyrilo instance, like setting the host of GAMS5.
        """
        self.authorization_service = AuthorizationService(host)
        self.digital_object_service = DigitalObjectService(host)
        self.ingest_service = IngestService(host, local_bagit_files_path=local_bagit_files_path)
        self.integration_service = IntegrationService(host)
        self.project_service = ProjectService(host)
        self.collection_service = CollectionService(host)
        self.host = host


    def login(self):
        """
        Logs in to the GAMS5 instance.
        """
        # first login
        auth_cookie = self.authorization_service.login()
        # set auth info on classes
        self.digital_object_service.auth = auth_cookie
        self.ingest_service.auth = auth_cookie
        self.integration_service.auth = auth_cookie
        self.project_service.auth = auth_cookie

    def list_objects(self, project_abbr: str) -> List[str]:
        """
        Lists all objects of defined project
        """

        return self.digital_object_service.list_objects(project_abbr)

    def save_object(self, id: str, project_abbr: str):
        """
        Creates a digital object 
        """
        return self.digital_object_service.save_object(id, project_abbr)

    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns a child object to a parent object
        """
        return self.digital_object_service.assign_child_objects(parent_id, children_ids, project_abbr)

    def delete_object(self, id: str, project_abbr: str):
        """
        Deletes a digital object
        """
        try:
            return self.digital_object_service.delete_object(id, project_abbr)
        except Exception as e:
            logging.error(f"Failed to delete object {id} in project {project_abbr}: {e}")

    def delete_objects(self, project_abbr: str):
        """
        Deletes all digital objects of a project
        """
        project_objects = self.list_objects(project_abbr)
        logging.info(f"Deleting now {len(project_objects)} objects for project {project_abbr}")
        for obj in project_objects:
            self.delete_object(obj, project_abbr)

    def ingest_bag(self, project_abbr: str, sip_folder_name: str):
        """
        Ingests defined folder from the local SIP structure.
        """
        self.ingest_service.ingest_bag(project_abbr, sip_folder_name)

    def ingest_bags(self, project_abbr: str):
        """
        Ingests all bags from the local bag structure.
        """
        self.ingest_service.ingest_bags(project_abbr)

    def integrate_project_objects(self, project_abbr: str):
        """
        Integrates all objects of a project
        """
        return self.integration_service.integrate_all(project_abbr)

    def disintegrate_project_objects(self, project_abbr: str):
        """
        Disintegrates all objects of a project
        """
        return self.integration_service.disintegrate_all(project_abbr)

    def integrate_project_object(self, project_abbr: str, id: str):
        """
        Integrates a single object of a project in gams-integration services.
        """
        return self.integration_service.integrate(project_abbr, id)

    def disintegrate_project_object(self, project_abbr: str, id: str):
        """
        Disintegrates a single object of a project in gams-integration services.
        """
        return self.integration_service.disintegrate(project_abbr, id)

    def ingest(self, project_abbr: str):
        """
        Performs a complete ingest operation based on the defined SIP folders.
        """

        # optionally delete all objects first
        # self.delete_objects(project_abbr)

        # delete all indices from dependend services
        # self.disintegrate_project_objects(project_abbr)

        # ingesting all bags from the local bag structure admin
        self.ingest_bags(project_abbr)


    def create_project(self, project_abbr: str, description: str):
        """
        Creates a new project with given abbreviation and description.
        """
        try:
            self.project_service.save_project(project_abbr, description)
        except ValueError as e:
            msg = f"Skipping project creation: Failed to create project: {e}"
            logging.error(msg)

    def update_project(self, project_abbr: str, description: str):
        """
        Updates a project.
        """
        self.project_service.update_project(project_abbr, description)

    def delete_project(self, project_abbr: str):
        """
        Deletes a project.
        """
        self.project_service.delete_project(project_abbr)

    def create_collection(self,project_abbr: str, collection_id: str, title: str, desc: str):
        """
        Creates a GAMS collection
        """
        self.collection_service.save_collection(
            project_abbr=project_abbr,
            collection_id=collection_id,
            title=title,
            desc=desc
        )

    def delete_collection(self, project_abbr: str, collection_id: str):
        """
        Deletes specified collection entry
        """
        self.collection_service.delete_collection(
            project_abbr=project_abbr,
            collection_id=collection_id
        )

    def setup_integration_services(self, project_abbr: str):
        """
        Triggers the integration of a project.
        """
        try:
            self.project_service.trigger_project_integration(project_abbr)
        except ConnectionError:
            pass
            msg = f"Skipping setup of integration service for project: Integration service already created: {project_abbr}"
            logging.warning(msg)

import logging
import os
from typing import List, Optional
from pyrilo.api.DigitalObject.DigitalObjectService import DigitalObjectService
from pyrilo.api.GamsApiClient import GamsApiClient
from pyrilo.app.IngestService import IngestService
from pyrilo.app.IntegrationService import IntegrationService
from pyrilo.api.Project.ProjectService import ProjectService
from pyrilo.api.auth.AuthorizationService import AuthorizationService
from pyrilo.exceptions import PyriloConflictError, PyriloNetworkError


class Pyrilo:
    """
    Provides abstractions for the usage of GAMS5 REST-API, like:
    - ingesting bags as digital objects and datastreams
    - creation of projects etc.
    """

    # Core components
    client: GamsApiClient
    host: str
    local_bagit_files_path: Optional[str]

    # Services
    digital_object_service: DigitalObjectService
    ingest_service: IngestService
    integration_service: IntegrationService
    authorization_service: AuthorizationService
    project_service: ProjectService

    def __init__(self,
                 local_bagit_files_path: str,
                 authorization_service: AuthorizationService,
                 digital_object_service: DigitalObjectService,
                 ingest_service: IngestService,
                 integration_service: IntegrationService,
                 project_service: ProjectService
                 ) -> None:

        self.local_bagit_files_path = local_bagit_files_path

        self.authorization_service = authorization_service
        self.digital_object_service = digital_object_service
        self.ingest_service = ingest_service
        self.integration_service = integration_service
        self.project_service = project_service

    def login(self, username: str = None, password: str = None):
        """
        Logs in to the GAMS5 instance.
        """
        # first login
        self.authorization_service.login(username, password)

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

        return self.digital_object_service.delete_object(id, project_abbr)

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
        if self.digital_object_service.object_exists(sip_folder_name, project_abbr):
            self.delete_object(sip_folder_name, project_abbr)
            logging.info(f"Successfully deleted existing object: {sip_folder_name} for ingest")


        self.ingest_service.ingest_bag(project_abbr, sip_folder_name)

    def ingest_bags(self, project_abbr: str):
        """
        Ingests all bags from the local bag structure.
        """

        if not self.local_bagit_files_path:
            raise ValueError("Local bag path is not configured.")

        failures = []

        for folder_name in os.listdir(self.local_bagit_files_path):
            # Basic filter (you might want to improve this)
            if not folder_name.startswith(project_abbr):
                continue

            try:
                logging.info(f"Starting ingest for: {folder_name}")
                self.ingest_bag(project_abbr, folder_name)
                logging.info(f"Successfully ingested: {folder_name}")
            except Exception as e:
                logging.error(f"FAILED to ingest {folder_name}: {e}")
                failures.append(folder_name)

        # Critical: If there were failures, we should probably let the caller know
        if failures:
            raise RuntimeError(f"Batch ingest completed with {len(failures)} errors: {failures}")

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

    def integrate_project_objects_custom_search(self, project_abbr: str):
        """
        Integrates all objects of a project to custom search service.
        """
        return self.integration_service.integrate_all_custom_search(project_abbr)

    def disintegrate_project_objects_custom_search(self, project_abbr: str):
        """
        Disintegrates all objects of a project from custom search service.
        """
        return self.integration_service.disintegrate_all_custom_search(project_abbr)

    def integrate_project_objects_plexus_search(self, project_abbr: str):
        """
        Integrates all objects of a project to plexus search service.
        """
        return self.integration_service.integrate_all_plexus_search(project_abbr)

    def disintegrate_project_objects_plexus_search(self, project_abbr: str):
        """
        Disintegrates all objects of a project from plexus search service.
        """
        return self.integration_service.disintegrate_all_plexus_search(project_abbr)

    def ingest(self, project_abbr: str):
        """
        Performs a complete ingest operation based on the defined SIP folders.
        """

        # optionally delete all objects first
        # self.delete_objects(project_abbr)

        # delete all indices from dependent services
        # self.disintegrate_project_objects(project_abbr)

        # ingesting all bags from the local bag structure admin
        self.ingest_bags(project_abbr)


    def create_project(self, project_abbr: str, description: str):
        """
        Creates a new project with given abbreviation and description.
        """
        self.project_service.save_project(project_abbr, description)

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

    def setup_integration_services(self, project_abbr: str):
        """
        Triggers the integration of a project.
        """
        try:
            self.project_service.trigger_project_integration(project_abbr)
        except PyriloConflictError:
            # THIS is the specific case we want to ignore (it already exists)
            msg = f"Integration service already setup for project: {project_abbr}"
            logging.info(msg)  # Info, not warning, since this is expected behavior
        except PyriloNetworkError:
            # Do NOT catch this silently. If the network is down, the user must know.
            # We let it bubble up, or re-raise with context.
            raise

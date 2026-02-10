import logging
import os
from pathlib import Path
from pyrilo.api.GamsApiClient import GamsApiClient
# Import the new service
from pyrilo.infrastructure.FileSystemService import FileSystemService

class IngestService:
    """
    Zips and sends bags to the GAMS5 REST-API using GamsApiClient.
    """

    client: GamsApiClient
    file_system: FileSystemService  # New dependency
    LOCAL_BAGIT_FILES_PATH: str

    # Updated constructor to accept file_system dependency
    def __init__(self,
                 client: GamsApiClient,
                 file_system: FileSystemService,
                 local_bagit_files_path: str = None) -> None:
        self.client = client
        self.file_system = file_system

        if local_bagit_files_path:
            self.LOCAL_BAGIT_FILES_PATH = local_bagit_files_path
        else:
            self.LOCAL_BAGIT_FILES_PATH = str(Path.cwd() / "bags")

        # We can leave this check here as a sanity check, or move it.
        # Since it's configuration validation, it's acceptable here.
        if not os.path.exists(self.LOCAL_BAGIT_FILES_PATH):
            logging.warning(f"Bag directory not found at: {self.LOCAL_BAGIT_FILES_PATH}")

    def ingest_bag(self, project_abbr: str, folder_name: str):
        """
        Ingests defined folder from the local bag structure.
        """
        folder_path = os.path.join(self.LOCAL_BAGIT_FILES_PATH, folder_name)
        logging.debug(f"Zipping folder {folder_path} ...")

        # This fixes the Windows bug and allows us to mock 'create_zip_from_folder' in tests.
        zip_content = self.file_system.create_zip_from_folder(folder_path)

        # Prepare for requests
        files_payload = {
            "subInfoPackZIP": ("bag.zip", zip_content, "application/zip")
        }
        data_payload = {
            "ingestProfile": "simple"
        }

        logging.debug(f"Requesting ingest for project {project_abbr} ...")

        self.client.post(
            f"projects/{project_abbr}/objects",
            files=files_payload,
            data=data_payload,
            timeout=100
        )

    def ingest_bags(self, project_abbr: str):
        """
        Walks through project directory and ingest the bags as individual objects.
        """
        # This makes it easy to mock an empty list or a specific list of folders in tests.
        try:
            subfolders = self.file_system.list_subdirectories(self.LOCAL_BAGIT_FILES_PATH)
        except Exception as e:
            logging.error(f"Could not list bags directory: {e}")
            return

        for folder_name in subfolders:
            try:
                if folder_name.startswith(project_abbr):
                    self.ingest_bag(project_abbr, folder_name)
            except Exception as e:
                logging.error(f"Failed to ingest bag {folder_name} for project {project_abbr}: {e}")
                continue
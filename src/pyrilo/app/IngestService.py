import logging
import os
import tempfile
from pathlib import Path
import zipfile
from pyrilo.api.GamsApiClient import GamsApiClient


class IngestService:
    """
    Zips and sends bags to the GAMS5 REST-API using GamsApiClient.
    """

    client: GamsApiClient
    LOCAL_BAGIT_FILES_PATH: str

    def __init__(self, client: GamsApiClient, local_bagit_files_path: str = None) -> None:
        self.client = client

        if local_bagit_files_path:
            self.LOCAL_BAGIT_FILES_PATH = local_bagit_files_path
        else:
            self.LOCAL_BAGIT_FILES_PATH = str(Path.cwd() / "bags")

        if not os.path.exists(self.LOCAL_BAGIT_FILES_PATH):
            logging.warning(f"Bag directory not found at: {self.LOCAL_BAGIT_FILES_PATH}")

    def ingest_bag(self, project_abbr: str, folder_name: str):
        """
        Ingests defined folder from the local bag structure.
        """
        folder_path = os.path.join(self.LOCAL_BAGIT_FILES_PATH, folder_name)
        logging.debug(f"Zipping folder {folder_path} ...")

        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tempf:
            with zipfile.ZipFile(tempf.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(os.path.join(root, file),
                                   os.path.relpath(os.path.join(root, file), folder_path))

            # Read the file back into memory
            tempf.seek(0)
            zip_content = tempf.read()

            # Prepare for requests
            files_payload = {
                "subInfoPackZIP": ("bag.zip", zip_content, "application/zip")
            }
            data_payload = {
                "ingestProfile": "simple"
            }

            logging.debug(f"Requesting ingest for project {project_abbr} ...")

            # We use the client to post. raise_errors=True is default.
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
        bags_dir = self.LOCAL_BAGIT_FILES_PATH
        for folder_name in os.listdir(bags_dir):
            if not os.path.isdir(os.path.join(bags_dir, folder_name)):
                continue

            try:
                if folder_name.startswith(project_abbr):
                    self.ingest_bag(project_abbr, folder_name)
            except Exception as e:
                logging.error(f"Failed to ingest bag {folder_name} for project {project_abbr}: {e}")
                continue
import logging
import os
import tempfile
from pathlib import Path
from pyrilo.PyriloStatics import PyriloStatics
import requests
import zipfile


class IngestService:
    """
    Zips and sends bags to the GAMS5 REST-API using requests.Session.
    """

    session: requests.Session
    host: str
    API_BASE_PATH: str
    LOCAL_BAGIT_FILES_PATH: str

    def __init__(self, session: requests.Session, host: str, local_bagit_files_path: str = None) -> None:
        self.session = session
        self.host = host
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"
        self.LOCAL_BAGIT_FILES_PATH = local_bagit_files_path

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

            # Read the file back into memory (as per original implementation)
            tempf.seek(0)
            zip_content = tempf.read()

            # Ingest zip file
            url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects"
            logging.debug(f"Requesting against {url} ...")

            # Prepare for requests: files dict and data dict
            files = {
                "subInfoPackZIP": ("bag.zip", zip_content, "application/zip")
            }
            data = {
                "ingestProfile": "simple"
            }

            # Requests automatically handles Content-Type and Boundary for multipart/form-data
            r = self.session.post(url, files=files, data=data, timeout=100)

            if r.status_code >= 400:
                msg = f"Failed to request against {url}. API response: {r.text}"
                raise ConnectionError(msg)

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
import logging
import os
import tempfile
from PyriloStatics import PyriloStatics
from urllib3 import encode_multipart_formdata, make_headers, request
import zipfile

from pyrilo.auth.AuthCookie import AuthCookie


class IngestService:
    """
    Zips and sends bags to the GAMS5 REST-API with correspondent http requests.
    """

    auth: AuthCookie | None = None
    host: str
    # do some error control? (should not contain trailing slashes etc.) 
    API_BASE_PATH: str


    def __init__(self, host: str, auth: AuthCookie | None = None) -> None:
        self.host = host
        self.auth = auth
        self.API_BASE_PATH = f"{host}{PyriloStatics.API_ROOT}"

    
    def ingest_bag(self, project_abbr: str, folder_name: str):
        """
        Ingests given given folder from the local bag structure.
        """
        
        # find folder? 

        # validate folder? 

        folder_path =  os.path.join(PyriloStatics.LOCAL_BAGIT_FILES_PATH, folder_name)
        logging.debug(f"Zipping folder {folder_path} ...")

        # zip files / folder
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tempf:
            with zipfile.ZipFile(tempf.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                                os.path.relpath(os.path.join(root, file), folder_path))
                        
            # ingest zip file
            url = f"{self.API_BASE_PATH}/projects/{project_abbr}/objects/"

            logging.debug(f"Requesting against {url} ...")

            # use cookie header if available
            headers = self.auth.build_auth_cookie_header() if self.auth else None
            body_form_data, content_type = self.create_multipart_formdata(tempf.read())
            headers["Content-Type"] = content_type

            # construct a multipart request via formdata
            r = request("POST", url, headers=headers, redirect=False, body=body_form_data, timeout=100)

            # include CSRF token? (NOT NECESSARY FROM PYTHON CLIENT?)

            if r.status >= 400:
                msg = f"Failed to request against {url}. API response: {r.json()}"
                raise ConnectionError(msg)
            else:
                logging.info(f"Successfully ingested folder {folder_name} for project {project_abbr}.")
            
    def ingest_bags(self, project_abbr: str):
        """
        Walks through project directory and ingest the bags as individual objects.
        """
        bags_dir = PyriloStatics.LOCAL_BAGIT_FILES_PATH
        for folder_name in os.listdir(bags_dir):
            # skip files
            if not os.path.isdir(os.path.join(bags_dir, folder_name)):
                continue

            self.ingest_bag(project_abbr, folder_name)
        

    def create_multipart_formdata(self, data):
        """
            Creates multipart formdata request body for the given data.

        """
        form_multipart = {
            "subInfoPackZIP": data,
            # TODO remove (is required atm)
            "ingestProfile": "simple"
        }

        body, content_type = encode_multipart_formdata(form_multipart, boundary=None)
        return body, content_type

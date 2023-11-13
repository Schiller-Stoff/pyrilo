from collections import OrderedDict
import io
import logging
import os
from pathlib import Path
import shutil
import tempfile
from statics.GAMS5APIStatics import GAMS5APIStatics
from urllib3 import encode_multipart_formdata, make_headers, request
import zipfile

class SubInfoPackService:
  """
  Handles submission information packages.
  """

  auth: tuple | None = None
  host: str
  # do some error control? (should not contain trailing slashes etc.) 
  API_BASE_PATH: str

  def __init__(self, host: str, auth: tuple | None = None) -> None:
    self.host = host
    self.auth = auth
    self.API_BASE_PATH = f"{host}{GAMS5APIStatics.API_ROOT}"

  def ingest_folder_object(self, project_abbr: str, folder_name: str):
    """
    Ingests a complete project structure.
    """
    
    # find folder? 

    # validate folder? 

    # zip folder?
    folder_path =  os.getcwd() + "/project/" + folder_name
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

        # construct headers
        headers = make_headers(basic_auth=f'{self.auth[0]}:{self.auth[1]}')
        body_form_data, content_type = self.create_multipart_formdata(tempf.read())
        headers["Content-Type"] = content_type

        # construct a multipart request via formdata
        r = request("POST", url, headers=headers, redirect=False, body=body_form_data)

        # include CSRF token? (NOT NECESSARY FROM PYTHON CLIENT?)

        if r.status >= 400:
            msg = f"Failed to request against {url}. API response: {r.json()}"
            raise ConnectionError(msg)
        else:
            logging.info(f"Successfully ingested folder {folder_name} for project {project_abbr}.")
            

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

  


import logging
import os
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

  def request_sip_files(project_abbr: str):
    """
    Requests all SIP files of a project from the gams-api.
    """
    raise NotImplementedError("Not implemented yet.")




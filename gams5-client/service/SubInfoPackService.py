import logging
import os
import tempfile

from service.content_model.TEIService import TEIService
from statics.GAMS5APIStatics import GAMS5APIStatics
from urllib3 import encode_multipart_formdata, make_headers, request
import zipfile
import os
import xml.etree.ElementTree as ET
from typing import Callable

class SubInfoPackService:
  """
  Handles submission information packages.
  """
  
  @staticmethod
  def walk_sip_folder(lambda_func: Callable[[str, str], None]):
    """
    Walks through all SIP files and calls given function for each folder. 
    :param lambda_func: function to call for each folder - gets the folderpath as first parameter and the path to the source file as second parameter
    """
    for folder_name in os.listdir(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH):
      folder_path = os.path.join(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH, folder_name)
      if os.path.isdir(folder_path):
        source_file_path = os.path.join(folder_path, GAMS5APIStatics.SIP_SOURCE_FILE_NAME)
        lambda_func(folder_path, source_file_path)

import logging
import os
import tempfile
from statics.GAMS5APIStatics import GAMS5APIStatics
from urllib3 import encode_multipart_formdata, make_headers, request
import zipfile
import os
from typing import Callable

class SubInfoPackService:
  """
  Handles submission information packages.
  """
  
  @staticmethod
  def walk_sip_folder(lambda_func: Callable[[str], None]):
    """
    Walks through all SIP files and calls given function for each folder. 
    :param lambda_func: function to call for each folder - gets the folderpath as parameter
    """
    for folder_name in os.listdir(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH):
      folder_path = os.path.join(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH, folder_name)
      if os.path.isdir(folder_path):
        lambda_func(folder_path)
    

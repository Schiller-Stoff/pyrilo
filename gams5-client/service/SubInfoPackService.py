import logging
import os
from statics.GAMS5APIStatics import GAMS5APIStatics
import os
import xml.etree.ElementTree as ET
from typing import Callable

class SubInfoPackService:
  """
  Handles submission information packages.
  """

  PROJECT_ABBR: str | None = None

  def __init__(self, project_abbr: str) -> None:
    self.PROJECT_ABBR = project_abbr
  
  def walk_sip_folder(self, lambda_func: Callable[[str, str, str], None], pattern: str = None):
    """
    Walks through all SIP files and calls given function for each folder. Skips all folder with underscore in name / path. 
    :param lambda_func: function to call for each folder - gets the folderpath as first parameter and the path to the source file as second parameter. Third parameter is the actually encountered folder pattern, like folder_demo --> "demo". Fourth parameter is the actual foldername.
    :param pattern: optional pattern to filter folders by name. By default filters all folders with underscore in name. If pattern is "*", all folders are processed.
    """
    for folder_name in os.listdir(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH):
      folder_path = os.path.join(GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH, folder_name)
      # skip if not a folder
      if not os.path.isdir(folder_path): 
        continue

      source_file_path = os.path.join(folder_path, GAMS5APIStatics.SIP_SOURCE_FILE_NAME)

      # if the pattern is a star -> all folders will be processed
      if pattern == "*":
        encountered_folder_pattern = ""
        if "_" in folder_name:
          encountered_folder_pattern = folder_path.split("_",1)[1]
        lambda_func(folder_path, source_file_path, encountered_folder_pattern, folder_name)

      # if pattern is not given, process all folders
      if pattern is None:
        # skip folders with underscore in name
        if "_" in folder_name: 
          continue
        lambda_func(folder_path, source_file_path, "", folder_name)

      # if pattern is given, process only folders with matching name  
      else:
        if "_" in pattern:
          msg = f"Pattern cannot contain an underscore. An underscore is prepended automatically. Given pattern: {pattern}"
          logging.error(msg)
          raise ValueError(msg)

        if folder_path.endswith("_" + pattern):
          # pass the actually encountered folder pattern to the lambda function
          encountered_folder_pattern = folder_path.split("_",1)[1]
          lambda_func(folder_path, source_file_path, encountered_folder_pattern, folder_name)


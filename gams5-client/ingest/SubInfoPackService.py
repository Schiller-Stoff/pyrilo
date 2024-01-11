import logging
import os
from ingest.statics.GAMS5APIStatics import GAMS5APIStatics
import os
from typing import Callable

class SubInfoPackService:
  """
  Handles submission information packages.
  """

  PROJECT_ABBR: str | None = None

  def __init__(self, project_abbr: str) -> None:
    self.PROJECT_ABBR = project_abbr
  
  # TODO: allow to set a content model --> only these folder are being looped
  def walk_sip_folder(self, lambda_func: Callable[[str, str, str, str, str], None], pattern: str = None, sip_folder_path: str = GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH, content_model: str = "*"):
    """
    Walks through all SIP files and calls given function for each folder. Skips all folder with underscore in name / path. 
    :param lambda_func: function to call for each folder - 
      gets the folderpath as first parameter and 
      Second parameter is the path to the source file. 
      Third parameter is the actually encountered folder pattern, like folder_demo --> "demo". 
      Fourth parameter is the actual foldername.
      Fifth parameter is the actually encountered content model, like folder_demo_tei --> "tei".
    :param pattern: optional pattern to filter folders by name. By default filters all folders with underscore in name. If pattern is "*", all folders are processed.
    :param sip_folder_path: optional path to the folder containing the SIPs. By default the local SIP folder is used.
    :param content_model: optional content model to filter folders by name. By default all folders are processed.
    """

    # TODO validate given sip_folder_path? e.g. is it even a path like object

    for folder_name in os.listdir(sip_folder_path):
      folder_path = os.path.join(sip_folder_path, folder_name)
      # skip if not a folder
      if not os.path.isdir(folder_path): 
        continue

      # small validation (if underscore is in folder name, it must be exactly two underscores)
      if "_" in folder_name:
        if folder_name.count("_") != 2:
          msg = f"Folder name must contain exactly two underscores. Given folder name: {folder_name}. For SIP: {sip_folder_path}"
          logging.error(msg)
          raise ValueError(msg)

      if content_model != "*":
        # skip folders that don't contain the given content model
        if ("_" + content_model) not in folder_name:
          continue

      source_file_path = os.path.join(folder_path, GAMS5APIStatics.SIP_SOURCE_FILE_NAME)

      # if the pattern is a star -> all folders will be processed
      if pattern == "*":
        encountered_folder_pattern = ""
        encountered_contentmodel_pattern = "tei"
        if folder_name.count("_") == 2:
          folder_path_parts = folder_name.split("_")
          encountered_contentmodel_pattern = folder_path_parts[1].lower()
          encountered_folder_pattern = folder_path_parts[2].lower()

        lambda_func(folder_path, source_file_path, encountered_folder_pattern, folder_name, encountered_contentmodel_pattern)

      # if pattern is not given, process all folders
      if pattern is None:
        # skip folders with underscore in name - TODO: better to skip all with two underscores?
        if "_" in folder_name: 
          continue
        lambda_func(folder_path, source_file_path, "", folder_name, "tei")

      # if pattern is given, process only folders with matching name  
      else:
        if "_" in pattern:
          msg = f"Pattern cannot contain an underscore. An underscore is prepended automatically. Given pattern: {pattern}"
          logging.error(msg)
          raise ValueError(msg)

        # TODO adapt - 
        if folder_path.endswith("_" + pattern):
          # pass the actually encountered folder pattern to the lambda function
          folder_path_parts = folder_name.split("_")
          encountered_contentmodel_pattern = folder_path_parts[1].lower()
          encountered_folder_pattern = folder_path_parts[2].lower()
          lambda_func(folder_path, source_file_path, encountered_folder_pattern, folder_name, encountered_contentmodel_pattern)


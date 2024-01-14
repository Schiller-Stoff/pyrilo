

import json
import logging
import os
from typing import Dict, List
from PyriloStatics import PyriloStatics
from extract.SIPService import SIPService
from PIL import Image

class SIPRefiner:
    """
    Changes the folders and files in the SIP, like enriching with metadata - creating additional 
    files (=datastreams) and folders, or removing files and folders.
    """

    PROJECT_ABBREVIATION: str
    SIP_SERVICE: SIPService

    def __init__(self, project_abbreviation):
        """
        Constructor.
        """
        self.PROJECT_ABBREVIATION = project_abbreviation
        self.SIP_SERVICE = SIPService(project_abbreviation)


    def refine(self):
        """
        Refines all SIPs in the local SIP folder.
        Meant to be overwritten by project specific subclasses.
        """
        # TODO add more?
        self.SIP_SERVICE.walk_sip_folder(self.process_tei_sip, content_model="tei")
        self.SIP_SERVICE.walk_sip_folder(self.process_tei_sip, content_model="lido")


    def generate_thumbnail(self, sip_folder_path: str):
        """
        Generates a thumbnail for a given sip folder if 
        """
        try:
            EXPECTED_IMAGE_FILE_PATH = os.path.join(sip_folder_path, PyriloStatics.THUMBNAIL_SIP_SOURCE_FILE_NAME)
            image = Image.open(EXPECTED_IMAGE_FILE_PATH)
            image.thumbnail((90,90))
            image.save(os.path.join(sip_folder_path, PyriloStatics.THUMBNAIL_FILE_NAME))
        except FileNotFoundError:
            logging.info(f"No image found in SIP folder at expected location for thumbnail generation: {EXPECTED_IMAGE_FILE_PATH}.")
            pass
        except IOError:
            logging.info(f"Failed to create thumbnail for SIP {sip_folder_path} {IOError}")
            pass


    def generate_search_index_json(self, entries: List[Dict[str, str]], sip_folder_path: str):
        """
        Generates a search index json file for a given list of dicts at given sip_folder_path
        :param entries: list of dicts containing the search index entries
        :param sip_folder_path: path to the sip folder
        """
        # TODO validate the entries here?
        # TODO validate muts contain id / _id?

        search_json_path = os.path.join(sip_folder_path, PyriloStatics.SIP_SEARCH_JSON_FILE_NAME)
        with open(search_json_path, "w", encoding="utf-8") as search_file:
            # setting ensure ascii to false to allow umlauts
            json.dump(entries, search_file, indent=4, ensure_ascii=False)

        logging.info(f"Generated search.json file for SIP at {search_json_path}.")


    def process_tei_sip(self, sip_folder_path: str, source_file_path: str, folder_pattern: str, folder_name: str, content_model: str):
        """
        TODO implement
        """
        logging.info("Processing TEI SIPs.")
        self.generate_thumbnail(sip_folder_path)
        pass
    
    def process_lido_sip(self, sip_folder_path: str, source_file_path: str, folder_pattern: str, folder_name: str, content_model: str):
        """
        TODO implement
        """
        logging.info("Processing LIDO SIPs.")
        self.generate_thumbnail(sip_folder_path)
        pass

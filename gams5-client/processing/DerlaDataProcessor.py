

from service.content_model.TEIService import TEIService
from service.SubInfoPackService import SubInfoPackService
from statics.GAMS5APIStatics import GAMS5APIStatics
from PIL import Image
import os
import logging
import json

class DerlaDataProcessor:
    """
    Handles / controls the data processing operations for the DERLA project.

    """

    def __init__(self):
        self.demo_data_processing()


    def process_sip_folder(self, sip_folder_path, source_file_path):
        """
        Demo lambda function for processing a SIP folder. (for DERLA)
        """
        MY_PROJECT = "demo"
        
        # creates thumbnails for the sips
        self.generate_thumbnail(sip_folder_path)    

        # creates search.json files for the sips
        self.generate_search_json(sip_folder_path)

        # project worker needs to decide which content model to use.
        # tei_service = TEIService(MY_PROJECT, source_file_path, sip_folder_path)
        


    def demo_data_processing(self):
        """
        Demo for data processing operations.
        """
        SubInfoPackService.walk_sip_folder(self.process_sip_folder)

    
    def generate_thumbnail(self, sip_folder_path: str):
        """
        Generates a thumbnail for a given sip folder if 
        """
        try:
            EXPECTED_IMAGE_FILE_PATH = os.path.join(sip_folder_path, GAMS5APIStatics.THUMBNAIL_SIP_SOURCE_FILE_NAME)
            image = Image.open(EXPECTED_IMAGE_FILE_PATH)
            image.thumbnail((90,90))
            image.save(os.path.join(sip_folder_path, GAMS5APIStatics.THUMBNAIL_FILE_NAME))
        except FileNotFoundError:
            logging.info(f"No image found in SIP folder at expected location for thumbnail generation: {EXPECTED_IMAGE_FILE_PATH}.")
            pass
        except IOError:
            logging.info(f"Failed to create thumbnail for SIP {sip_folder_path} {IOError}")
            pass


    def generate_search_json(self, sip_folder_path: str):
        """
        Generates a search.json file for a given SIP folder.
        """

        # TODO needs to be adapted
        search_data = {
            "title": "Search Results",
            "results": [
                {
                    "id": 1,
                    "title": "Result 1",
                    "description": "This is the first search result."
                },
                {
                    "id": 2,
                    "title": "Result 2",
                    "description": "This is the second search result."
                },
                {
                    "id": 3,
                    "title": "Result 3",
                    "description": "This is the third search result."
                }
            ]
        }

        search_json_path = os.path.join(sip_folder_path, "search.json")
        with open(search_json_path, "w") as search_file:
            json.dump(search_data, search_file, indent=4)

        logging.info(f"Generated search.json file for SIP at {search_json_path}.")


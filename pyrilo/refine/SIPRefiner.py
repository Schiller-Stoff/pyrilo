

import json
import logging
import os
from typing import Dict, List
from PyriloStatics import PyriloStatics
from extract.SIPService import SIPService
from PIL import Image
import mimetypes
from extract.SIPFileMetadata import SIPFileMetadata

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
        self.create_iiif_manifest_from_sip_folder(sip_folder_path)
        pass
    
    def process_lido_sip(self, sip_folder_path: str, source_file_path: str, folder_pattern: str, folder_name: str, content_model: str):
        """
        TODO implement
        """
        logging.info("Processing LIDO SIPs.")
        self.generate_thumbnail(sip_folder_path)
        self.create_iiif_manifest_from_sip_folder(sip_folder_path)
        pass


    def create_iiif_manifest_from_sip_folder(self, object_id: str, sip_folder_path: str):
        """
        Creates a IIIF manifest for a given generic SIP folder. Assigning object id / manifest attributes by file
        and folder convention.
        
        """
        pass

        # image_dicts = {"images": [] }

        # # loop over all files in the current SIP folder at sip_folder_path
        # for file_name in os.listdir(sip_folder_path):
        #     file_path = os.path.join(sip_folder_path, file_name)
        #     # skip if not a file
        #     if os.path.isdir(file_path): 
        #         continue
  
        #     # check if sipfile metadata creates an image
        #     image_mimetypes = ["image/jpeg", "image/png", "image/tiff", "image/gif"]
        #     # split in root and extension
        #     file_root, file_extension = os.path.splitext(file_name)
        #     # guess mimetype from path
        #     file_mimetype = mimetypes.guess_type(os.path.join(sip_folder_path, file_name))[0]
        #     # skip if not an image
        #     if file_mimetype not in image_mimetypes:
        #         continue
            
        #     # skip thumbnail
        #     if file_root.lower() == "thumbnail":
        #         continue

        #     # TODO add correct dsid
        #     img_dsid = file_root

        #     # construct iiif url
        #     # TODO think about localhost 18080 addressation?
        #     iiif_url = f"http://localhost:18080/iiif/3/{self.PROJECT_ABBREVIATION}%2F{object_id}%2F{img_dsid}%2Finfo.json"
        
        #     # creation of IIIF manifests --> need to know about the pid!
        #     image_dicts["images"].append(iiif_url)

        # # write manifest.json
        # json_content = json.dumps(image_dicts)
        # file_to_write = sip_folder_path + os.path.sep + "manifest.json"
        # with open(file_to_write, 'w') as file:
        #     file.write(json_content)


    def create_iiif_manifest(self, image_datastreams: List[SIPFileMetadata], object_id: str, sip_folder_path: str):
        """
        Creates a IIIF manifest for a given list of image datastreams.
        :param image_datastreams: list of SIPFileMetadata objects
        :param object_id: id of the object
        :param sip_folder_path: path to the SIP folder
        """
        # TODO add logging?
        manifest = {
            "@context": "http://iiif.io/api/presentation/3/context.json",
            "type": "Manifest",
            # id will be set later
            # "id": "https://iiif.io/api/cookbook/recipe/0001-mvm-image/manifest.json",
            # TODO add propper label
            "label": {
                "en": [
                    "Single Image Example"
                ]
            },
            "items": [] 
            
        }

        for image_datastream in image_datastreams:
            

            # fail safe: check mimetypes -> throw error if not an image

            # check if sipfile metadata creates an image
            # image_mimetypes = ["image/jpeg", "image/png", "image/tiff", "image/gif"]
            
            # skip if not an image
            # if image_datastream.mimetype not in image_mimetypes:
            #     continue

            # construct iiif url
            # TODO think about localhost 18080 addressation?
            iiif_url = f"http://localhost:18080/iiif/3/{self.PROJECT_ABBREVIATION}%2F{object_id}%2F{image_datastream.dsid}/info.json"
        
            # TODO server address is dangerous!
            manifest["id"] = f"http://localhost:18085/api/v1/projects/{self.PROJECT_ABBREVIATION}/objects/{object_id}/datastreams/{image_datastream.dsid}/content"

            # TODO refactor IIIF manifest!
            # creation of IIIF manifests --> need to know about the pid!
            item = {
                "id": iiif_url, 
                "type": "Canvas",
                "height": 1800,
                "width": 1200
                    
            }
            
            manifest["items"].append(item)

        # write manifest.json
        json_content = json.dumps(manifest)
        file_to_write = sip_folder_path + os.path.sep + "manifest.json"
        with open(file_to_write, 'w') as file:
            file.write(json_content)

        
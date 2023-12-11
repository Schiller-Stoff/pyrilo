from datetime import datetime
from service.content_model.GAMSXMLNamespaces import GAMSXMLNamespaces
from service.content_model.TEISIP import TEISIP
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

    PROJECT_ABBREVIATION = "demo"

    def __init__(self):
        self.demo_data_processing()


    def process_sip_folder(self, sip_folder_path, source_file_path):
        """
        Demo lambda function for processing a SIP folder. (for DERLA)
        """
        
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

        tei_sip = TEISIP(self.PROJECT_ABBREVIATION, sip_folder_path)
        # default operations provided by the TEISIP
        title = tei_sip.resolve_title()
        id = tei_sip.resolve_pid()
        desc = tei_sip.resolve_sip_description()
        types = tei_sip.resolve_terms()
        # DERLA specific operations
        location = self.extract_geo_location(tei_sip)
        creation_date = self.extract_creation_date(tei_sip)

        # solr dict to be written to json file
        search_data = [{
            "title": title,
            "id": id,
            "desc": desc,
            "types": types,
            "location": location,
            "creation_date_dt": creation_date,
        }]

        search_json_path = os.path.join(sip_folder_path, GAMS5APIStatics.SIP_SEARCH_JSON_FILE_NAME)
        with open(search_json_path, "w", encoding="utf-8") as search_file:
            # setting ensure ascii to false to allow umlauts
            json.dump(search_data, search_file, indent=4, ensure_ascii=False)

        logging.info(f"Generated search.json file for SIP at {search_json_path}.")

    
    def extract_geo_location(self, tei_sip: TEISIP):
        """
        Extracts the geo location from a DERLA TEISIP object.
        """
        geo_elems = tei_sip.XML_ROOT.findall(".//geo", GAMSXMLNamespaces.TEI_NAMESPACES)

        if len(geo_elems) < 2:
            raise Exception(f"Not enough geo elements found in TEI SIP. {tei_sip.SIP_FOLDER_PATH}")
        
        if geo_elems[0].text is None or geo_elems[1].text is None:
            raise Exception(f"Geo elements in TEI SIP are empty. {tei_sip.SIP_FOLDER_PATH}")

        return f"{geo_elems[0].text},{geo_elems[1].text}" 


    def extract_creation_date(self, tei_sip: TEISIP):
        """
        Extracts the creation date from a DERLA TEISIP object.
        """

        creation_date_elem = tei_sip.XML_ROOT.find(".//date[@type='creation']", GAMSXMLNamespaces.TEI_NAMESPACES)

        creation_date = "01.01.2023"
        # check if tei element is not none and if the text is not none
        if creation_date_elem is not None:
            if creation_date_elem.text is not None:
                creation_date = creation_date_elem.text

        # if the creation date is only a year, we add a default month and day
        if len(creation_date) <= 4:
            logging.info(f"Creation date element is invalid in TEI SIP. {tei_sip.SIP_FOLDER_PATH}")
            creation_date = f"01.01.{creation_date}"


        input_format = "%d.%m.%Y"
        output_format = "%Y-%m-%dT%H:%M:%SZ"

        # Convert input date string to a datetime object
        parsed_date = datetime.strptime(creation_date, input_format)

        # Format the datetime object in the desired output format
        solr_date = parsed_date.strftime(output_format)

        return solr_date
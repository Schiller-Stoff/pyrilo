
import xml.etree.ElementTree as ET
import utils.xml_operations as xml_operations
from statics.GAMS5APIStatics import GAMS5APIStatics
import os
from service.content_model.SIPMetadata import SIPMetadata
from service.content_model.SIPFileMetadata import SIPFileMetadata
import logging
import uuid

class SIP:
    """
    Operates on the transformation from SIP to bags.
    Handles all SIP related operations, like creating a json serialization.
    """

    PROJECT_ABBR: str
    XML_ROOT: ET.Element
    SIP_FOLDER_PATH: str
    SIP_SOURCE_FILE_PATH: str
    SUBTYPE: str


    def __init__(self, project_abbr: str, sip_folder_path: str, subtype: str = "") -> None:
        self.PROJECT_ABBR = project_abbr
        self.SIP_FOLDER_PATH = sip_folder_path
        self.SIP_SOURCE_FILE_PATH = os.path.join(sip_folder_path, GAMS5APIStatics.SIP_SOURCE_FILE_NAME)
        self.XML_ROOT = self.read_xml(self.SIP_SOURCE_FILE_PATH)
        self.SUBTYPE = subtype


    def read_xml(self, path: str) -> ET.Element:
        """
        Parses given xml file and returns root element.
        """

        # open file a string and clean it -> otherwiese ETree wil very often fail at parsing
        with open(path, 'r', encoding="utf8") as file:
            content = file.read()
            content = xml_operations.clean_xml_string(content)
            return xml_operations.parse_xml(content)
        

    def write_sip_object_to_json(self, sip_object_metadata: SIPMetadata, target_path: str):
        """
        Transforms given sip object to json and writes it to the given path. 
        """

        # TODO add some error checks? e.g. if target_path is valid

        with open(target_path, 'w') as file:
            file.write(sip_object_metadata.serialize_to_json())
        
        logging.info(f"Succesffully wrote sip.json to path: {target_path}")


    def extract_full_text(self):
        """
        Extracts the full text from the TEI document.
        """
        return ET.tostring(self.XML_ROOT, encoding='utf-8', method='text').decode("utf-8")
    

    def extract_metadata(self) -> SIPMetadata:
        """
        Creates default metadata for a SIP without an implemented content model Subclass.
        Extracts metadata from the SIP. 
        Method is meant to be overridden by subclasses and acts as default.
        """

        logging.warning("Method should be overridden by a subclass for the content model. No metadata extraction implemented for this content model. Creating dummy metadata object.")

        print("*** " + self.SIP_FOLDER_PATH)

        object_id = self.SIP_FOLDER_PATH.rsplit('/', 1)[-1]
        title = f"Object for project: {self.PROJECT_ABBR}"
        creator = f"{self.PROJECT_ABBR}"
        description = f"Object created without implemented metadata extraction for the content model. For SIP: {self.SIP_FOLDER_PATH}"

        object_metadata = SIPMetadata(
            id=object_id, 
            title=title, 
            creator=creator, 
            description=description,
            object_type="Base object", 
            publisher=creator, 
            rights="CC BY-SA 4.0",
            types=[self.SUBTYPE],
            contentFiles=[],
        )

        return object_metadata

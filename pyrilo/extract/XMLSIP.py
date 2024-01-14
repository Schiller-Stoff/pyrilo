
import xml.etree.ElementTree as ET
import extract.utils.xml_operations as xml_operations
from extract.SIP import SIP
import logging

class XMLSIP(SIP):
    """
    Extracts metadata from a XMLSIP folder and it's contained files.
    
    Operates on the transformation from XMLSIP to bags.
    Handles all XMLSIP related operations, like creating a json serialization.
    """

    XML_ROOT: ET.Element

    def __init__(self, project_abbr: str, sip_folder_path: str, subtype: str = "") -> None:
        SIP.__init__(self, project_abbr, sip_folder_path, subtype)
        self.XML_ROOT = self.read_xml(self.SIP_SOURCE_FILE_PATH)

        
    def read_xml(self, path: str) -> ET.Element:
        """
        Parses given xml file and returns root element.
        """
        # TODO add logging

        # open file a string and clean it -> otherwiese ETree wil very often fail at parsing
        with open(path, 'r', encoding="utf8") as file:
            content = file.read()
            content = xml_operations.clean_xml_string(content)
            return xml_operations.parse_xml(content)
        

    def extract_full_text(self):
        """
        Extracts the full text from the TEI document.
        """
        # TODO add logging
        return ET.tostring(self.XML_ROOT, encoding='utf-8', method='text').decode("utf-8")
    
import logging
import xml.etree.ElementTree as ET
from content_model.GAMSXMLNamespaces import GAMSXMLNamespaces
import utils.xml_operations as xml_operations

class TEIService:
    """
    Handles all TEI related operations, like extracting pid from a TEI document.

    """

    def read_xml(self, path: str) -> ET.Element:
        """
        Parses given xml file and returns root element.
        """
        return xml_operations.parse_xml(path)


    def extract_metadata(xml_root: ET.Element):
        """
        Extracts metadata from a TEI document.

        """
        # read out pid
        # read out description
        # read out title
        # read out creator
        # ...

        pid_idno_elem = xml_root.find(".//idno[@type='pid']", GAMSXMLNamespaces.TEI_NAMESPACES)
        id = pid_idno_elem.text

        title_title_elem = xml_root.find(".//titleStmt/title", GAMSXMLNamespaces.TEI_NAMESPACES)
        title = title_title_elem.text

        logging.info("Extracted pid: " + id)
        logging.info("Extracted title: " + title)

        # raise NotImplementedError("Not implemented yet.")


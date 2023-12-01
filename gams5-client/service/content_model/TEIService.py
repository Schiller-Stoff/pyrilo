import dataclasses
import json
import logging
import xml.etree.ElementTree as ET
from typing import List
from service.content_model.ContentModels import ContentModels
from service.content_model.SIPMetadata import SIPMetadata
from service.content_model.SIPFileMetadata import SIPFileMetadata
from service.content_model.GAMSXMLNamespaces import GAMSXMLNamespaces
import utils.xml_operations as xml_operations

class TEIService:
    """
    Handles all TEI related operations, like extracting pid from a TEI document.

    """

    @staticmethod
    def read_xml(path: str) -> ET.Element:
        """
        Parses given xml file and returns root element.
        """

        # open file a string and clean it -> otherwiese ETree wil very often fail at parsing
        with open(path, 'r', encoding="utf8") as file:
            content = file.read()
            content = xml_operations.clean_xml_string(content)
            return xml_operations.parse_xml(content)
        
    @staticmethod    
    def write_sip_object_to_json(sip_object_metadata: SIPMetadata, target_path: str):
        """
        Transforms given sip object to json and writes it to the given path. 
        """

        # TODO add some error checks? e.g. if target_path is valid

        with open(target_path, 'w') as file:
            file.write(sip_object_metadata.serialize_to_json())
        
        logging.info(f"Succesffully wrote sip.json to path: {target_path}")


    @staticmethod
    def extract_metadata(xml_root: ET.Element) -> SIPMetadata:
        """
        Extracts metadata from a TEI document.

        """
        # read out pid
        # read out description
        # read out title
        # read out creator
        # ...

        pid_idno_elem = xml_root.find(".//idno[@type='PID']", GAMSXMLNamespaces.TEI_NAMESPACES) 
        if pid_idno_elem is None:
            raise ReferenceError("No pid found in TEI document.")
        
        id = pid_idno_elem.text

        title_title_elem = xml_root.find(".//titleStmt/title", GAMSXMLNamespaces.TEI_NAMESPACES)
        if title_title_elem is None:
            raise ReferenceError("No title found in TEI document.")
        
        title = title_title_elem.text

        logging.info("Extracted pid: " + id)
        logging.info("Extracted title: " + title)


        object_metadata = SIPMetadata(
            id=id, 
            title=title, 
            creator="TODO", 
            description="TODO",
            object_type=ContentModels.TEI, 
            publisher="TODO", 
            rights="TODO",
            files=[]
        )

        # process images defined in the TEI document
        image_files = TEIService._handle_tei_images(xml_root)
        for image_file in image_files:
            object_metadata.files.append(image_file)
        
        # TODO process other files defined in the TEI document

        logging.info(f"Extracted metadata from TEI document. {object_metadata}")
        return object_metadata


    @staticmethod
    def _handle_tei_images(xml_root: ET.Element):
        """
        Extracts image metadata from a TEI document.
        """
        
        graphic_elems = xml_root.findall(".//facsimile/graphic", GAMSXMLNamespaces.TEI_NAMESPACES)

        # check if there are images defined in the TEI document
        if (graphic_elems is None) or (len(graphic_elems) == 0):
            raise ReferenceError("No images found in TEI document.")
        

        image_datastreams: List[SIPFileMetadata] = []

        for graphic_elem in graphic_elems:
            url = TEIService._resolve_image_url_to_bagpath(graphic_elem)
            mimetype = TEIService._resolve_mimetype(graphic_elem)
            
            # TODO - somehow etree does not recognize the xml:id attribute's namespace
            dsid = graphic_elem.get("{http://www.w3.org/XML/1998/namespace}id")
            logging.info(f"{graphic_elem.attrib}")
            if dsid is None:
                raise ReferenceError("No xml:id found on image <graphic> element.")

            # TODO ectract description, title, creator, rights, publisher, size, mimetype

            cur_image_datastream = SIPFileMetadata(
                dsid=dsid, 
                bagpath=url, 
                title="TODO", 
                mimetype=mimetype, 
                creator="TODO", 
                description="TODO", 
                rights="TODO", 
                publisher="TODO", 
                size="TODO"
            )
            
            logging.info(f"Found image {cur_image_datastream} in TEI document.")
            image_datastreams.append(cur_image_datastream)
        
        logging.info(f"Found {len(graphic_elems)} images in TEI document.")

        return image_datastreams
    

    @staticmethod
    def _resolve_image_url_to_bagpath(graphic_elem: ET.Element) -> str:
        """
        Reads out the defined graphic element's url and resolves it to the expected bag-path.
        Like from "file:///1.JPG" to "data/content/1.JPG"
        """
        url = graphic_elem.get("url")
        if url is None:
            raise ReferenceError("No url attribute found on image <graphic> element.")
        
        if "file:///" in url:
            url = url.replace("file:///", "data/content/")
            logging.info(f"Resolved TEI's graphic image url to: {url}")
        # TODO add some checks what should not be included inside the urL?
            
        # TODO rewrite url to the expected bag-path directly here?
        # TODO maybe check if the url contains "file:///" and points outside of the SIP? -> throw an exception?
        # TODO what if the url does no contain "file:///"? -> throw an exception?

        return url

    @staticmethod
    def _resolve_mimetype(graphic_elem: ET.Element) -> str:
        """
        Reads out the defined graphic element's mimetype.
        """
        mimetype = graphic_elem.get("mimeType")
        if mimetype is None:
            raise ReferenceError("No mimetype attribute found on image <graphic> element in given TEI document")
        
        # TODO could add some checks if the mimetyoe is valid / if the mimetype actually corresponds to the file etc.

        return mimetype
    
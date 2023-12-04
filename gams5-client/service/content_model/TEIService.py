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

    PROJECT_ABBR: str
    XML_ROOT: ET.Element

    def __init__(self, project_abbr: str, xml_path: str) -> None:
        self.PROJECT_ABBR = project_abbr
        self.XML_ROOT = self.read_xml(xml_path)


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


    def extract_metadata(self) -> SIPMetadata:
        """
        Extracts metadata from a TEI document.

        """
        # read out pid
        # read out description
        # read out title
        # read out creator
        # ...

        # TODO move to own method
        pid_idno_elem = self.XML_ROOT.find(".//idno[@type='PID']", GAMSXMLNamespaces.TEI_NAMESPACES) 
        if pid_idno_elem is None:
            raise ReferenceError("No pid found in TEI document.")
        
        id = pid_idno_elem.text

        # TODO transfer to own method
        title_title_elem = self.XML_ROOT.find(".//titleStmt/title", GAMSXMLNamespaces.TEI_NAMESPACES)
        if title_title_elem is None:
            raise ReferenceError("No title found in TEI document.")
        
        title = title_title_elem.text

        logging.info("Extracted pid: " + id)
        logging.info("Extracted title: " + title)

        description = self.resolve_sip_description()
        
        creator = self._resolve_tei_creator()

        object_metadata = SIPMetadata(
            id=id, 
            title=title, 
            # TODO add processing of missing statements!
            creator=creator, 
            description=description,
            object_type=ContentModels.TEI, 
            publisher="TODO", 
            rights="TODO",
            contentFiles=[]
        )

        # add TEI_SOURCE.xml as content file
        object_metadata.contentFiles.append(
            SIPFileMetadata(
                # TODO tink about actual data assignment
                title="TEI_SOURCE", 
                dsid="TEI_SOURCE", 
                bagpath="data/content/TEI_SOURCE.xml", 
                mimetype="text/xml",
                # TODO add actual size 
                size=9999999,
                # TODO add processing of missing statements! 
                creator=creator, 
                description="TODO", 
                rights="TODO", 
                publisher="TODO", 
            )
        )

        # process images defined in the TEI document
        image_files = self._handle_tei_images()
        for image_file in image_files:
            object_metadata.contentFiles.append(image_file)
        
        # TODO process other files defined in the TEI document

        logging.info(f"Extracted metadata from TEI document. {object_metadata}")
        return object_metadata


    def resolve_sip_description(self):
        """
        Reads out the defined description of the TEI.
        Assigns a default description if no description is defined.
        """
        # TODO what about logging?
        p_description = self.XML_ROOT.find(".//encodingDesc/editorialDecl/p", GAMSXMLNamespaces.TEI_NAMESPACES)
        if p_description is None:
            # TODO default should be something like (Digital object of the xyz projcet) or something like that
            return "TODO TODO TODO"
        else:
            return p_description.text

    def _resolve_tei_creator(self):
        """
        Reads out the defined creator of the TEI.
        Assigns a default creator if no creator is defined.
        """
        DEFAULT_CREATOR = f"{self.PROJECT_ABBR} (GAMS-project)"
        marcrelator_author = self.XML_ROOT.find(".//author[@ana='marcrelator:aut']", GAMSXMLNamespaces.TEI_NAMESPACES)
        if marcrelator_author is None:
            return f"{self.PROJECT_ABBR} (GAMS-project)"
        
        forename_elem = marcrelator_author.find("./persName/forename")
        surname_elem = marcrelator_author.find("./persName/surname")
        if (forename_elem is None) or (surname_elem is None):
            return DEFAULT_CREATOR
        
        return DEFAULT_CREATOR


    def _handle_tei_images(self):
        """
        Extracts image metadata from a TEI document.
        """
        
        graphic_elems = self.XML_ROOT.findall(".//facsimile/graphic", GAMSXMLNamespaces.TEI_NAMESPACES)

        # check if there are images defined in the TEI document
        if (graphic_elems is None) or (len(graphic_elems) == 0):
            raise ReferenceError("No images found in TEI document.")
        

        image_datastreams: List[SIPFileMetadata] = []

        for graphic_elem in graphic_elems:
            url = self._resolve_image_url_to_bagpath(graphic_elem)
            mimetype = self._resolve_mimetype(graphic_elem)
            
            # TODO - somehow etree does not recognize the xml:id attribute's namespace
            dsid = graphic_elem.get("{http://www.w3.org/XML/1998/namespace}id")
            logging.info(f"{graphic_elem.attrib}")
            if dsid is None:
                raise ReferenceError("No xml:id found on image <graphic> element.")

            # TODO ectract description, title, creator, rights, publisher, size, mimetype

            title = self.resolve_file_title(graphic_elem, dsid)
            size = self.resolve_file_size(graphic_elem)

            cur_image_datastream = SIPFileMetadata(
                dsid=dsid, 
                bagpath=url, 
                title=title, 
                mimetype=mimetype,
                # TODO add processing of missing statements! 
                creator="TODO", 
                description="TODO", 
                rights="TODO", 
                publisher="TODO", 
                size=size
            )

            logging.info(f"Found image {cur_image_datastream} in TEI document.")
            image_datastreams.append(cur_image_datastream)
        
        logging.info(f"Found {len(graphic_elems)} images in TEI document.")

        return image_datastreams
    

    def _resolve_image_url_to_bagpath(self, graphic_elem: ET.Element) -> str:
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

    
    def _resolve_mimetype(self, graphic_elem: ET.Element) -> str:
        """
        Reads out the defined graphic element's mimetype.
        """
        mimetype = graphic_elem.get("mimeType")
        if mimetype is None:
            raise ReferenceError("No mimetype attribute found on image <graphic> element in given TEI document")
        
        # TODO could add some checks if the mimetyoe is valid / if the mimetype actually corresponds to the file etc.

        return mimetype

    
    def resolve_file_title(self, graphic_elem: ET.Element, dsid: str) -> str:
        """
        Reads out the defined graphic element's title. If no title is defined, the dsid is used as title.
        """
        # TODO currently there is no title defined in the TEI document?
        
        # TODO could add some checks if the title is valid / if the title actually corresponds to the file etc.

        return dsid
    
    
    def resolve_file_size(self, graphic_elem: ET.Element) -> str:
        """
        Reads out the defined graphic element's size.
        """
        # TODO would need to be generated? -> maybe not needed?
        
        # TODO could add some checks if the size is valid / if the size actually corresponds to the file etc.

        return 9999999
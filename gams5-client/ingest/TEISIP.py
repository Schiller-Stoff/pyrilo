import logging
import xml.etree.ElementTree as ET
from typing import Dict, List
from api.GAMS5APIStatics import GAMS5APIStatics
from ingest.ContentModels import ContentModels
from ingest.SIPMetadata import SIPMetadata
from ingest.SIPFileMetadata import SIPFileMetadata
from ingest.GAMSXMLNamespaces import GAMSXMLNamespaces
import os
from ingest.SIP import SIP

class TEISIP(SIP):
    """
    Extracts metadata from a SIP folder and it's contained files.

    Handles extractiom related to the TEI content model, like extracting pid from a specific xml-element.
    """

    def __init__(self, project_abbr: str, sip_folder_path: str, subtype: str = "") -> None:
        SIP.__init__(self, project_abbr, sip_folder_path, subtype)
        

    def extract_metadata(self) -> SIPMetadata:
        """
        Extracts metadata from a TEI document.

        """
        
        id = self.resolve_pid()
        title = self.resolve_title()
        description = self.resolve_sip_description()
        creator = self._resolve_tei_creator()

        # add type information 
        types = []
        if self.SUBTYPE != "":
            types.append(self.SUBTYPE)

        object_metadata = SIPMetadata(
            id=id, 
            title=title, 
            # TODO add processing of missing statements!
            creator=creator, 
            description=description,
            object_type=ContentModels.TEI, 
            publisher="TODO", 
            rights="TODO",
            types=types,
            contentFiles=[],
        )

        # create a dictionary of datastream-ids with content file metadata
        # needs to be mapped later on to contentFiles
        files_dict = self.resolve_datastream_files(ignore_files=["1.JPG", "2.JPG"])

        # process images defined in the TEI document
        image_files = self._handle_tei_images()
        for image_file in image_files:
            files_dict[image_file.dsid] = image_file

        # everything in dictionary is being added as content file
        for key in files_dict.keys():
            object_metadata.contentFiles.append(files_dict[key])

        logging.info(f"Extracted metadata from TEI document. {object_metadata}")
        return object_metadata


    def resolve_pid(self):
        """
        Reads out the defined pid of the TEI.
        """
        pid_xpath = ".//idno[@type='PID']"
        pid_idno_elem = self.XML_ROOT.find(pid_xpath, GAMSXMLNamespaces.TEI_NAMESPACES) 
        if pid_idno_elem is None:
            raise ReferenceError(f"No pid at {pid_xpath} found in TEI document. At SIP: {self.SIP_FOLDER_PATH}")        
        
        if pid_idno_elem.text is None:
            raise ReferenceError(f"No text assigned to pid indo {pid_xpath} in TEI document. At SIP: {self.SIP_FOLDER_PATH}") 

        return pid_idno_elem.text
    
    def resolve_title(self):
        """
        Reads out the defined title of the TEI.
        """
        title_xpath = ".//titleStmt/title"
        title_title_elem = self.XML_ROOT.find(title_xpath, GAMSXMLNamespaces.TEI_NAMESPACES) 
        if title_title_elem is None:
            raise ReferenceError(f"No title at {title_xpath} found in TEI document.")        
        
        if title_title_elem.text is None:
            raise ReferenceError(f"No text assigned to title {title_xpath} in TEI document.") 

        return title_title_elem.text
    
    def resolve_terms(self):
        """
        Reads out the defined terms of the TEI.
        Removes duplicates.
        """
        all_terms_xpath = ".//term"
        all_terms_elem = self.XML_ROOT.findall(all_terms_xpath, GAMSXMLNamespaces.TEI_NAMESPACES)
        if len(all_terms_elem) == 0:
            return [] 
        
        terms = []
        for term_elem in all_terms_elem:
            if term_elem.text is not None:
                terms.append(term_elem.text)
            else:
                logging.warning(f"Found empty term in TEI document at {term_elem}. Selected all terms at {all_terms_xpath}")

        # removing potential duplicates
        terms_set = set(terms)
        terms = list(terms_set)
        return terms

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
        
        graphic_elems_xpath = ".//facsimile/graphic"

        graphic_elems = self.XML_ROOT.findall(graphic_elems_xpath, GAMSXMLNamespaces.TEI_NAMESPACES)

        # check if there are images defined in the TEI document
        if (graphic_elems is None) or (len(graphic_elems) == 0):
            logging.info(f"No images found in TEI document for SIP at {self.SIP_FOLDER_PATH} with xpath {graphic_elems_xpath}")
            return []
        
        image_datastreams: List[SIPFileMetadata] = []

        for graphic_elem in graphic_elems:
            url = self._resolve_image_url_to_bagpath(graphic_elem)
            mimetype = self._resolve_mimetype(graphic_elem)
            
            # TODO - somehow etree does not recognize the xml:id attribute's namespace
            dsid = graphic_elem.get("{http://www.w3.org/XML/1998/namespace}id")
            logging.info(f"{graphic_elem.attrib}")
            if dsid is None:
                raise ReferenceError(f"No xml:id found on image <graphic> element. For sip at {self.SIP_FOLDER_PATH} with xpath {graphic_elems_xpath}")

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
    
    def resolve_thumbnail(self) -> List[SIPFileMetadata]:
        """
        Checks if a thumbnail is defined in the SIP folder and returns it as SIPFileMetadata if available0
        :return: SIPFileMetadata of the thumbnail if available, otherwise an empty list
        """
        
        thumbnail_path = os.path.join(self.SIP_FOLDER_PATH, GAMS5APIStatics.THUMBNAIL_FILE_NAME)
        logging.info(f"Checking if thumbnail exists at {thumbnail_path}")
        if not os.path.exists(thumbnail_path):
            return []
        
        sip_file_description = SIPFileMetadata(
                    bagpath="/data/content/" + GAMS5APIStatics.THUMBNAIL_FILE_NAME, 
                    dsid=GAMS5APIStatics.THUMBNAIL_DATASTREAM_ID, 
                    mimetype="image/jpeg",
                    creator=f"{self.PROJECT_ABBR} GAMS-project",
                    description=f"Thumbnail generated for the {self.PROJECT_ABBR} project.",
                    publisher="TODO",
                    rights="TODO",
                    size=9999999,
                    title=GAMS5APIStatics.THUMBNAIL_FILE_NAME
            )
        
        logging.info(f"Created thumbnail entry {sip_file_description}")

        return [sip_file_description]

    def resolve_search_json(self):
        """
        Checks if a search json is defined in the SIP folder and returns it as SIPFileMetadata if available
        :return: SIPFileMetadata of the search json if available, otherwise an empty list
        """
        search_json_path = os.path.join(self.SIP_FOLDER_PATH, GAMS5APIStatics.SIP_SEARCH_JSON_FILE_NAME)
        logging.info(f"Checking if thumbnail exists at {search_json_path}")
        if not os.path.exists(search_json_path):
            return []
        
        sip_file_description = SIPFileMetadata(
                    bagpath="/data/content/" + GAMS5APIStatics.SIP_SEARCH_JSON_FILE_NAME, 
                    dsid=GAMS5APIStatics.SIP_SEARCH_JSON_DATASTREAM_ID, 
                    mimetype="application/json",
                    creator=f"{self.PROJECT_ABBR} GAMS-project",
                    description=f"Base search json generated for the {self.PROJECT_ABBR} project.",
                    publisher="TODO",
                    rights="TODO",
                    size=9999999,
                    title=GAMS5APIStatics.SIP_SOURCE_DATASTREAM_ID
            )

        return [sip_file_description]
    
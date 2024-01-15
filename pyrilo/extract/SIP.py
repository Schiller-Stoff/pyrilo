import os
from typing import Dict, List
from PyriloStatics import PyriloStatics
import logging
import mimetypes
from extract.SIPMetadata import SIPMetadata
from extract.SIPFileMetadata import SIPFileMetadata


class SIP:
    """
    Extracts metadata from a SIP folder and it's contained files.	
    """

    PROJECT_ABBR: str
    SIP_FOLDER_PATH: str
    SIP_SOURCE_FILE_PATH: str
    SUBTYPE: str

    def __init__(self, project_abbr: str, sip_folder_path: str, subtype: str = "") -> None:
        """
        Constructor.
        """
        self.PROJECT_ABBR = project_abbr
        self.SIP_FOLDER_PATH = sip_folder_path
        self.SIP_SOURCE_FILE_PATH = os.path.join(sip_folder_path, PyriloStatics.SIP_SOURCE_FILE_NAME)
        self.SUBTYPE = subtype


    def write_metadata_to_json(self, sip_object_metadata: SIPMetadata, target_path: str):
        """
        Transforms given sip object to json and writes it to the given path. 
        """

        # TODO add some error checks? e.g. if target_path is valid

        with open(target_path, 'w') as file:
            file.write(sip_object_metadata.serialize_to_json())
        
        logging.info(f"Succesffully wrote sip.json to path: {target_path}")


    def extract_metadata(self) -> SIPMetadata:
        """
        Creates default metadata for a XMLSIP without an implemented content model Subclass.
        Extracts metadata from the XMLSIP. 
        Method is meant to be overridden by subclasses and acts as default.
        """

        logging.warning("Method should be overridden by a subclass for the content model. No metadata extraction implemented for this content model. Creating dummy metadata object.")

        # TODO splitting if folder path looks dangerous!
        object_id = self.SIP_FOLDER_PATH.rsplit('/', 1)[-1]
        title = f"Object for project: {self.PROJECT_ABBR}"
        creator = f"{self.PROJECT_ABBR}"
        description = f"Object created without implemented metadata extraction for the content model. For XMLSIP: {self.SIP_FOLDER_PATH}"

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

        # TODO add logging

        
        datastream_files = self.resolve_datastream_files()
        # map to contentFiles array
        for file in datastream_files:
            object_metadata.contentFiles.append(datastream_files[file])

        return object_metadata
    

    def resolve_datastream_files(self, ignore_files: List[str] = []) -> Dict[str, SIPFileMetadata]:
        """"
        Resolves all datastream files in the XMLSIP folder and returns them as a dictionary of SIPFileMetadata objects.
        :param ignore_files: List of file names that should be ignored.
        :returns Returns a dictionary of all datastream files with the dsid as key and a SIPFileMetadata object as value.
        """
        sip_file_descriptions: Dict[str, SIPFileMetadata] = {}
        # go through files in XMLSIP (skip every file that is not described via elements in the TEI document)
        # Loop through the SIPs folder
        for file_name in os.listdir(self.SIP_FOLDER_PATH):
            # all folders are being ignored
            if not os.path.isfile(os.path.join(self.SIP_FOLDER_PATH, file_name)):
                continue
            # optionally ignore certain files
            if file_name in ignore_files:
                logging.debug(f"Ignoring file to map as sip contentFile: {file_name}")
                continue    

            # split in root and extension
            file_root, file_extension = os.path.splitext(file_name)
            # guess mimetype from path
            file_mimetype = mimetypes.guess_type(os.path.join(self.SIP_FOLDER_PATH, file_name))[0]

            file_size = os.path.getsize(os.path.join(self.SIP_FOLDER_PATH, file_name))

            sip_file_description = SIPFileMetadata(
                # TODO /data/content -> should come form PyriloStatics?
                    bagpath="/data/content/" + file_name, 
                    dsid=file_root, 
                    mimetype=file_mimetype,
                    creator=self.PROJECT_ABBR,
                    description="Datastream for GAMS project " + self.PROJECT_ABBR + ".",
                    publisher=f"{self.PROJECT_ABBR} GAMS project",
                    rights=f"CC BY 4.0",
                    size=file_size,
                    title=f"Datastream containing the {file_name} file"
            )

            

            sip_file_descriptions[file_root] = sip_file_description

        return sip_file_descriptions
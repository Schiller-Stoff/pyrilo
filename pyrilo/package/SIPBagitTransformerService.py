import datetime
import logging
import os
import shutil
from extract.XMLSIP import XMLSIP
from extract.TEISIP import TEISIP
from extract.GMLSIP import GMLSIP
from PyriloStatics import PyriloStatics
from extract.SIPService import SIPService
from extract.SIP import SIP

class SIPBagitTransformerService:
    """
    This class is responsible for transforming a project's SIP to the required bagit format.	
    """

    PROJECT_ABBR: str | None = None
    SIP_SERVICE: SIPService

    def __init__(self, project_abbr: str):
        self.PROJECT_ABBR = project_abbr
        self.SIP_SERVICE = SIPService(project_abbr)
    
    def create_bag_files(self, bag_folder_path: str):
        """
        Creates basic bag files like bagit.txt and bag-info.txt
        """
        # Generate bagit.txt file
        bagit_file_path = os.path.join(bag_folder_path, "bagit.txt")
        with open(bagit_file_path, "w") as bagit_file:
            bagit_file.write("BagIt-Version: 0.97\n")
            bagit_file.write("Tag-File-Character-Encoding: UTF-8\n")

        # Generate bagit-info.txt file
        bagit_info_file_path = os.path.join(bag_folder_path, "bag-info.txt")
        with open(bagit_info_file_path, "w") as bagit_info_file:
            bagit_info_file.write("Bag-Software-Agent: Pyrilo\n")
            bagit_info_file.write("Bagging-Date: {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d")))
            # TODO add checksum here
            bagit_info_file.write("Payload Oxum: [SOME HASH]\n")
            # bagit_info_file.write("Contact-Email: example@example.com\n")
            # bagit_info_file.write("External-Description: Demo Bag\n")
            # bagit_info_file.write("External-Identifier: demo-bag\n")

    def create_bagit_checksum_files(self, bag_folder_path: str):
        """
        Creates checksum files for the bagit format.
        """
        # TODO add real logic for creating checksum files
        
        # Generate manifest-md5.txt file
        manifest_md5_file_path = os.path.join(bag_folder_path, "manifest-md5.txt")
        with open(manifest_md5_file_path, "w") as manifest_md5_file:
            # TODO checksum 
            manifest_md5_file.write("data/content/TEI_SOURCE.xml HASH\n")


    def transform(self, project_abbr: str):
        """
        Transforms all project files to the bagit format.
        TODO: rename! --> creates the base folder structure in the first place!
        """
        # delete all child folder inside bags folder
        self.delete_child_folders(PyriloStatics.LOCAL_BAGIT_FILES_PATH)
        # Loop through the SIPs folder
        self.SIP_SERVICE.walk_sip_folder(self._build_bag, pattern="*", content_model="*")


    def _build_bag(self, folder_path: str, source_file_path: str, encountered_folder_pattern: str, folder_name: str, content_model: str):
        """
        Build a singular bag from a SIP folder.
        Parameters are passed by the SIPService.
        """

        # TODO think about method implementation - many things might be included in SIPService.py

        # all files on folder root level are ignored
        if os.path.isfile(os.path.join(PyriloStatics.LOCAL_SIP_FOLDERS_PATH, folder_name)):
            return

        # Create the corresponding bags folder if it does not exist
        cur_bag_folder_path = os.path.join(PyriloStatics.LOCAL_BAGIT_FILES_PATH, folder_name)
        os.makedirs(cur_bag_folder_path, exist_ok=True)

        # Copy contents from SIP folder to the data/content directory inside the generated bag
        sip_folder_path = os.path.join(PyriloStatics.LOCAL_SIP_FOLDERS_PATH, folder_name)
        data_folder_path = os.path.join(cur_bag_folder_path, "data" + os.path.sep + "content")
        shutil.copytree(sip_folder_path, data_folder_path, dirs_exist_ok=True)

        # create meta folder for bagit
        meta_folder_path = os.path.join(cur_bag_folder_path, "data" + os.path.sep + "meta")
        os.makedirs(meta_folder_path, exist_ok=True)

        
        sip = None
        # process xml based SIPs
        if self.SIP_SERVICE.contains_source_xml(sip_folder_path):
            if content_model == "tei":
                sip = TEISIP(self.PROJECT_ABBR, sip_folder_path, encountered_folder_pattern)
            elif content_model == "":
                sip = TEISIP(self.PROJECT_ABBR, sip_folder_path, encountered_folder_pattern)
            elif content_model == "gml":
                sip = GMLSIP(self.PROJECT_ABBR, sip_folder_path, encountered_folder_pattern)
            else:
                sip = XMLSIP(self.PROJECT_ABBR, sip_folder_path, encountered_folder_pattern)
        # process not xml based SIPSs
        else:
            sip = SIP(self.PROJECT_ABBR, sip_folder_path, encountered_folder_pattern)
 

        sip_object = sip.extract_metadata()
        sip.write_sip_object_to_json(sip_object, os.path.join(meta_folder_path, "sip.json"))

        # Create basic bag files
        self.create_bag_files(cur_bag_folder_path)
        self.create_bagit_checksum_files(cur_bag_folder_path)

        logging.info(f"Successfully transformed SIP {folder_name} to bag {cur_bag_folder_path}.")

    def delete_child_folders(self, cur_bag_folder_path: str):
        """
        Deletes all folders inside given path
        """
        for folder_name in os.listdir(cur_bag_folder_path):
            folder_path = os.path.join(cur_bag_folder_path, folder_name)
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)

import datetime
import logging
import os
import shutil
from statics.GAMS5APIStatics import GAMS5APIStatics


class SIPBagitTransformerService:
    """
    This class is responsible for transforming a project's SIP to the required bagit format.	
    """

    def __init__(self):
        pass

    def validate(self, input_data):
        raise NotImplementedError()

    def save(self, output_data):
        raise NotImplementedError()
    
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
            bagit_info_file.write("Payload Oxum: [SOME HASH]\n")
            # bagit_info_file.write("Contact-Email: example@example.com\n")
            # bagit_info_file.write("External-Description: Demo Bag\n")
            # bagit_info_file.write("External-Identifier: demo-bag\n")

    def create_bagit_checksum_files(self, bag_folder_path: str):
        """
        Creates checksum files for the bagit format.
        """
        # TODO add real logic for creating cheksum files
        
        # Generate manifest-md5.txt file
        manifest_md5_file_path = os.path.join(bag_folder_path, "manifest-md5.txt")
        with open(manifest_md5_file_path, "w") as manifest_md5_file:
            manifest_md5_file.write("data/content/TEI_SOURCE.xml HASH\n")


    def transform(self):
        """
        Transforms all project files to the bagit format.
        """

        # Get the path of the SIPs folder
        sips_folder = GAMS5APIStatics.LOCAL_SIP_FOLDERS_PATH

        # Get the path of the bags folder
        bags_folder = GAMS5APIStatics.LOCAL_BAGIT_FILES_PATH

        # Loop through the SIPs folder
        for folder_name in os.listdir(sips_folder):
            # all files on folder root level are ignored
            if os.path.isfile(os.path.join(sips_folder, folder_name)):
                continue

            # Create the corresponding bags folder
            # TODO reneame variable - better cur_bag_folder_path
            bags_folder_path = os.path.join(bags_folder, folder_name)
            os.makedirs(bags_folder_path, exist_ok=True)

            # Copy contents from SIP folder to the data directory inside the generated bag
            sip_folder_path = os.path.join(sips_folder, folder_name)
            data_folder_path = os.path.join(bags_folder_path, "data")
            shutil.copytree(sip_folder_path, data_folder_path, dirs_exist_ok=True)

            # Create basic bag files
            self.create_bag_files(bags_folder_path)
            self.create_bagit_checksum_files(bags_folder_path)

            logging.info(f"Successfully transformed SIP {folder_name} to bag {bags_folder}.")

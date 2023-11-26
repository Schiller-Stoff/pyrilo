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
            # Create the corresponding bags folder
            bags_folder_path = os.path.join(bags_folder, folder_name)
            os.makedirs(bags_folder_path, exist_ok=True)

            # Copy contents from SIP folder to the data directory inside the generated bag
            sip_folder_path = os.path.join(sips_folder, folder_name)
            data_folder_path = os.path.join(bags_folder_path, "data")
            shutil.copytree(sip_folder_path, data_folder_path)



from service.content_model.TEIService import TEIService
from service.SubInfoPackService import SubInfoPackService


class DerlaDataProcessor:
    """
    Handles / controls the data processing operations for the DERLA project.

    """

    def __init__(self):
        self.demo_data_processing()


    def process_sip_folder(self, folder_path, source_file_path):
        """
        Demo lambda function for processing a SIP folder. (for DERLA)
        """
        MY_PROJECT = "demo"
        # project worker needs to decide which content model to use.
        tei_service = TEIService(MY_PROJECT, source_file_path)
        print(tei_service.XML_ROOT)


    def demo_data_processing(self):
        """
        Demo for data processing operations.
        """
        SubInfoPackService.walk_sip_folder(self.process_sip_folder)

    

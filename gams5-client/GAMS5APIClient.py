from service.SubInfoPackService import SubInfoPackService
from service.DigitalObjectService import DigitalObjectService
from service.SIPBagitTransformerService import SIPBagitTransformerService
from service.BagService import BagService
from service.IntegrationService import IntegrationService
from typing import List
from service.content_model.TEIService import TEIService

class GAMS5APIClient:
    """
    Provides abstractions for the usage of the gams5-api, like:
    - creating digital objects
    - requesting lists of datastreams for a digital object etc.
    """

    digital_object_service: DigitalObjectService
    sub_info_pack_service: SubInfoPackService
    sip_bagit_transformer_service: SIPBagitTransformerService
    bag_service: BagService
    integration_service: IntegrationService

    def __init__(self, host: str) -> None:
        self.digital_object_service = DigitalObjectService(host)
        self.bag_service = BagService(host)
        self.sub_info_pack_service = SubInfoPackService(host)
        self.sip_bagit_transformer_service = SIPBagitTransformerService()
        self.integration_service = IntegrationService(host)

    def configure_auth(self, user_name: str, user_pw: str):
        """
        Configures authentication for state changing operations via the REST-API.
        """
        self.digital_object_service.auth = (user_name, user_pw)
        self.bag_service.auth = (user_name, user_pw)
        self.integration_service.auth = (user_name, user_pw)

    def list_objects(self, project_abbr: str) -> List[str]:
        """
        Lists all objects of defined project
        """

        return self.digital_object_service.list_objects(project_abbr)
    
    def save_object(self, id: str, project_abbr: str):
        """
        Creates a digital object 
        """
        return self.digital_object_service.save_object(id, project_abbr)
    
    def delete_object(self, id: str, project_abbr: str):
        """
        Deletes a digital object
        """
        return self.digital_object_service.delete_object(id, project_abbr)
    
    def delete_objects(self, project_abbr: str):
        """
        Deletes all digital objects of a project
        """
        return self.digital_object_service.delete_objects(project_abbr)

    def ingest_bag(self, project_abbr: str, sip_folder_name: str):
        """
        Ingests defined folder from the local SIP structure.
        """
        self.bag_service.ingest_bag(project_abbr, sip_folder_name)

    def ingest_bags(self, project_abbr: str):
        """
        Ingests all bags from the local bag structure.
        """
        self.bag_service.ingest_bags(project_abbr)

    def transform_sips_to_bags(self, project_abbr: str):
        """
        Transforms all SIPs to the bagit format.
        """
        return self.sip_bagit_transformer_service.transform(project_abbr)
    
    def request_sip_files(self, project_abbr: str):
        """
        Requests all SIP files from the GAMS5-API and stores it in local folder structure
        """
        return self.sub_info_pack_service.request_sip_files(project_abbr)
    
    def integrate_project_objects(self, project_abbr: str):
        """
        Integrates all objects of a project
        """
        return self.integration_service.integrate_all(project_abbr)
    
    def disintegrate_project_objects(self, project_abbr: str):
        """
        Disintegrates all objects of a project
        """
        return self.integration_service.disintegrate_all(project_abbr)
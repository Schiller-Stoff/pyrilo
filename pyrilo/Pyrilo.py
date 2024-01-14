from extract.SIPService import SIPService
from api.DigitalObjectService import DigitalObjectService
from package.SIPBagitTransformerService import SIPBagitTransformerService
from package.BagService import BagService
from api.IntegrationService import IntegrationService
from typing import List

class Pyrilo:
    """
    Provides abstractions for the usage of GAMS5 REST-API, like:
    - ingesting SIPs as digital objects and datastreams
    - check method names for more
    """

    digital_object_service: DigitalObjectService
    sip_bagit_transformer_service: SIPBagitTransformerService
    bag_service: BagService
    integration_service: IntegrationService

    def __init__(self, host: str, project_abbr: str) -> None:
        self.digital_object_service = DigitalObjectService(host)
        self.bag_service = BagService(host)
        self.sip_bagit_transformer_service = SIPBagitTransformerService(project_abbr)
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
    

    def assign_child_objects(self, parent_id: str, children_ids: List[str], project_abbr: str):
        """
        Assigns a child object to a parent object
        """
        return self.digital_object_service.assign_child_objects(parent_id, children_ids, project_abbr)

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
    
    def integrate_project_object(self, project_abbr: str, id: str):
        """
        Integrates a single object of a project in gams-integration services.
        """
        return self.integration_service.integrate(project_abbr, id)
    

    def disintegrate_project_object(self, project_abbr: str, id: str):
        """
        Disintegrates a single object of a project in gams-integration services.
        """
        return self.integration_service.disintegrate(project_abbr, id)
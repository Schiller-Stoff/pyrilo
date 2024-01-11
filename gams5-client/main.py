
import logging
import os
from refine.DerlaDataProcessor import DerlaDataProcessor
from api.GAMS5APIStatics import GAMS5APIStatics
from ingest.SubInfoPackService import SubInfoPackService
from GAMS5APIClient import GAMS5APIClient

def setup_client(project_abbr: str) -> GAMS5APIClient:
    log_file_path = f"{os.getcwd()}/logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG, filemode='w')

    # example usage of the client
    # TODO configuring - maybe for handling auth thats not a good idea? e.g. GET requesting should possible all the time VS state changing operations
    # need to throw an error. --> maybe own configure_auth() method?
    client = GAMS5APIClient("http://localhost:18085", project_abbr)
    # configure authentication ins separate method.
    client.configure_auth("admin", "admin")
    return client


def demo_create_bags_and_ingest_them(pyrilo: GAMS5APIClient, MY_PROJECT: str):
    """
    Demo for creating bags and ingesting them directly afterwards.
    
    """
    # demo for transforming local SIPs to bagit format
    pyrilo.transform_sips_to_bags(MY_PROJECT)
    
    # optionally delete all objects first
    pyrilo.delete_objects(MY_PROJECT)

    # delete all indices from dependend services
    pyrilo.disintegrate_project_objects(MY_PROJECT)

    # demo for ingesting all bags from the local bag structure 
    pyrilo.ingest_bags(MY_PROJECT)

    # demo index all
    pyrilo.integrate_project_objects(MY_PROJECT)


if __name__ == "__main__":

    MY_PROJECT = "demo"

    pyrilo = setup_client(MY_PROJECT)
    
    
    
    # found_objects = pyrilo.list_objects(MY_PROJECT)
    # print(found_objects) 

    # pyrilo.save_object("demo4", MY_PROJECT)

    # pyrilo.ingest_bag(MY_PROJECT, "demo1")
    # pyrilo.delete_object("hsa.letter.1", MY_PROJECT)

    # create bags from sips strcucture and directly ingest them
    # demo_create_bags_and_ingest_them(pyrilo, MY_PROJECT)

    # pyrilo.delete_objects(MY_PROJECT)

    

    
    # test_contentmodels(pyrilo)


    # demo call for tansforming project sips to bags
    # pyrilo.transform_sips_to_bags(MY_PROJECT)


    # Integration operations.
    #
    # pyrilo.integrate_project_objects(MY_PROJECT)
    # pyrilo.disintegrate_project_objects(MY_PROJECT)

    # pyrilo.integrate_project_object(MY_PROJECT, "o:derla.vor146")
    # pyrilo.disintegrate_project_object(MY_PROJECT, "o:derla.vor146")


    # pyrilo.save_object("context:derlapers", MY_PROJECT)

    # demo assignment of child objects
    # pyrilo.assign_child_objects("context:derlapers", ["o:derla.persvor", "o:derla.perssty"], MY_PROJECT)


    DerlaDataProcessor()
    # pyrilo.transform_sips_to_bags(MY_PROJECT)
    demo_create_bags_and_ingest_them(pyrilo, MY_PROJECT)

    
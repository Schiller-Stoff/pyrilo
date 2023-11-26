
import logging
import os
from GAMS5APIClient import GAMS5APIClient

def setup_client() -> GAMS5APIClient:
    log_file_path = f"{os.getcwd()}/logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    # example usage of the client
    # TODO configuring - maybe for handling auth thats not a good idea? e.g. GET requesting should possible all the time VS state changing operations
    # need to throw an error. --> maybe own configure_auth() method?
    client = GAMS5APIClient("http://localhost:18085")
    # configure authentication ins separate method.
    client.configure_auth("admin", "admin")
    return client


def demo_create_bags_and_ingest_them(pyrilo: GAMS5APIClient):
    """
    Demo for creating bags and ingesting them directly afterwards.
    
    """
    # demo for transforming local SIPs to bagit format
    pyrilo.transform_sips_to_bags()
    
    # optionally delete all objects first
    pyrilo.delete_objects(MY_PROJECT)

    # demo for ingesting all bags from the local bag structure 
    pyrilo.ingest_bags(MY_PROJECT)



def demo_ingest_bag():
    pass


if __name__ == "__main__":

    pyrilo = setup_client()
    
    
    MY_PROJECT = "demo"
    # found_objects = pyrilo.list_objects(MY_PROJECT)
    # print(found_objects) 

    # pyrilo.save_object("demo4", MY_PROJECT)

    # pyrilo.ingest_bag(MY_PROJECT, "demo1")
    # pyrilo.delete_object("hsa.letter.1", MY_PROJECT)

    # create bags from sips strcucture and directly ingest them
    demo_create_bags_and_ingest_them(pyrilo)

    # pyrilo.delete_objects(MY_PROJECT)
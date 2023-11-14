
import logging
import os
from GAMS5APIClient import GAMS5APIClient


if __name__ == "__main__":

    log_file_path = f"{os.getcwd()}/logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG)

    # example usage of the client
    MY_PROJECT = "demo"
    # TODO configuring - maybe for handling auth thats not a good idea? e.g. GET requesting should possible all the time VS state changing operations
    # need to throw an error. --> maybe own configure_auth() method?
    client = GAMS5APIClient("http://localhost:18085")
    # configure authentication ins separate method.
    client.configure_auth("admin", "admin")

    # found_objects = client.list_objects(MY_PROJECT)
    # print(found_objects) 

    # client.save_object("demo4", MY_PROJECT)

    client.ingest_bag(MY_PROJECT, "hsaletter1")
    # client.delete_object("hsa.letter.1", MY_PROJECT)
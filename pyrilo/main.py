
import logging
import os
from PyriloStatics import PyriloStatics
from extract.SIPService import SIPService
from Pyrilo import Pyrilo

def setup():
    # log_file_path = f"{os.getcwd()}/logs/app.log"
    # TODO refactor this malformed path!
    log_file_path = f"{os.getcwd()}/../logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG, filemode='w')



if __name__ == "__main__":
    # setup logging etc.
    setup()

    MY_PROJECT = "demo"

    ### INGEST ###
    # connect to GAMS5 instance
    pyrilo = Pyrilo("http://localhost:18085", MY_PROJECT)
    # login
    pyrilo.login()

    pyrilo.create_project(MY_PROJECT, "Demo project for testing purposes")
    # pyrilo.delete_project("hupfi")


    # ingest SIPs
    pyrilo.ingest(MY_PROJECT)


    # pyrilo.transform_sips_to_bags(MY_PROJECT)

    # pyrilo.ingest_bag(MY_PROJECT, "vor57")

    
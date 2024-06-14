
import logging
import os
from Pyrilo import Pyrilo
import pathlib
from pyrilo.PyriloStatics import PyriloStatics


def setup():
    pathlib.Path(__file__)
    # get the path to the log file based on location of main.py
    log_file_path = PyriloStatics.LOCAL_PROJECT_ROOT_PATH + os.sep + "logs" + os.sep + "app.log"

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


    # pyrilo.integrate_project_objects(MY_PROJECT)

    # print(pyrilo.list_objects(MY_PROJECT))
    # pyrilo.delete_object("o:derla.vor10", MY_PROJECT)

    # pyrilo.ingest_bag(MY_PROJECT, "vor57")

    

import logging
import os
from refine.DerlaSIPRefiner import DerlaSIPRefiner
from PyriloStatics import PyriloStatics
from extract.SIPService import SIPService
from Pyrilo import Pyrilo

def setup():
    log_file_path = f"{os.getcwd()}/logs/app.log"

    # setup logging
    logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.DEBUG, filemode='w')



if __name__ == "__main__":
    # setup logging etc.
    setup()

    MY_PROJECT = "demo"
    
    # refinement of SIPs
    DerlaSIPRefiner(MY_PROJECT).refine()

    ### INGEST ###
    # connect to GAMS5 instance
    pyrilo = Pyrilo("http://localhost:18085", MY_PROJECT)
    # login
    pyrilo.configure_auth("admin", "admin")
    # ingest SIPs
    pyrilo.ingest(MY_PROJECT)

    
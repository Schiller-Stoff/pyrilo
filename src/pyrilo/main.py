
import logging
from .Pyrilo import Pyrilo
import pathlib

def setup():
    pathlib.Path(__file__)

    # setup logging
    logging.basicConfig( encoding='utf-8', level=logging.INFO)

    # alternatively, use the following to log to console
    # log_file_path = PyriloStatics.LOCAL_PROJECT_ROOT_PATH + os.sep + "logs" + os.sep + "app.log"
    # logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.INFO, filemode='w')

def main():
    """ Main function """
    # setup logging etc.
    setup()

    MY_PROJECT = "hsa"

    ### INGEST ###
    # connect to GAMS5 instance
    pyrilo = Pyrilo("http://localhost:18085", MY_PROJECT)
    # login
    pyrilo.login()

    pyrilo.create_project(MY_PROJECT, "Demo project for testing purposes")


    # pyrilo.setup_integration_services(MY_PROJECT)

    # ingest SIPs
    pyrilo.ingest(MY_PROJECT)

    pyrilo.integrate_project_objects(MY_PROJECT)

    # pyrilo.disintegrate_project_objects(MY_PROJECT)



    # pyrilo.integrate_project_objects(MY_PROJECT)

    # print(pyrilo.list_objects(MY_PROJECT))
    # pyrilo.delete_object("o:derla.vor10", MY_PROJECT)

    # delete objects of a project
    # pyrilo.delete_objects(MY_PROJECT)

    # pyrilo.ingest_bag(MY_PROJECT, "vor57")

# pyrilo.disintegrate_project_objects(MY_PROJECT)

# pyrilo.integrate_project_object(MY_PROJECT, "o:derla.vor10")

# pyrilo.disintegrate_project_object(MY_PROJECT, "o:derla.vor10")




# if __name__ == "__main__":
#     main()
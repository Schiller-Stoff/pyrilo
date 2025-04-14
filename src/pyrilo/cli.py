import click
import logging
from pyrilo.Pyrilo import Pyrilo

#
pyrilo: Pyrilo = Pyrilo("http://localhost:18085")

@click.group()
@click.option("--host", "-h", default="http://localhost:18085", help="The host of the GAMS5 instance")
@click.option("--bag_root", "-r", default="", help="Root folder path (as string) of the bagit files")
def cli(host: str, bag_root: str):
    """
    Pyrilo is a command line tool for managing your GAMS5 project.

    """
    logging.basicConfig( encoding='utf-8', level=logging.INFO)

    if bag_root:
        pyrilo.configure(host, bag_root)
    else:
        pyrilo.configure(host)

    pyrilo.login()


@cli.command(name="ingest", help="Ingest bags as digital objects and datastream for a project")
@click.argument("project", required=True)
def ingest(project: str):
    pyrilo.ingest(project)
    pyrilo.integrate_project_objects(project)


@cli.command(name="create_project", help="Creates a project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
def create_project(project: str, desc: str):
    pyrilo.create_project(project, desc)

@cli.command(name="update_project", help="Updates an existing project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
def update_project(project: str, desc: str):
    pyrilo.update_project(project, desc)

@cli.command(name="delete_objects", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
def delete_objects(project: str):
    pyrilo.delete_objects(project)

@cli.command(name="delete_object", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.argument("object_id", required=True)
def delete_object(project:str, object_id: str):
    pyrilo.delete_object(object_id, project)

@cli.command(name="create_collection", help="Creates a collection of digital objects on the GAMS-API.")
@click.argument("project", required=True)
@click.argument("id", required=True)
@click.argument("title", required=True)
@click.argument("desc", required=False)
def create_collection(project: str, id: str, title: str, desc: str):
    """
    Creates a GAMS collection of digital objects.
    A collection must have an "owning project".
    """
    pyrilo.create_collection(project, id, title, desc)

@cli.command(name="delete_collection", help="Deletes a collection of digital objects on the GAMS-API.")
@click.argument("project", required=True)
@click.argument("id", required=True)
def delete_collection(project: str, id: str):
    """
    Deletes a GAMS collection
    """
    pyrilo.delete_collection(
        project_abbr=project,
        collection_id=id
    )

@click.command(name="sync", help="Syncs a project with GAMS: Deletes all objects (and performs disintegration), ingests new objects and integrates them")
@click.argument("project", required=True)
def sync(project: str):
    # TODO remove temporary solution? (creation of project if not existent)
    pyrilo.create_project(project, "Demo project for testing purposes")
    pyrilo.setup_integration_services(project)
    pyrilo.disintegrate_project_objects(project)
    pyrilo.delete_objects(project)
    pyrilo.ingest(project)
    pyrilo.integrate_project_objects(project)

@cli.command(name="integrate", help="Integrates data of digital objects of a project with additional GAMS services like solr")
@click.argument("project", required=True)
def integrate(project: str):
    pyrilo.integrate_project_objects(project)

@click.command(name="disintegrate", help="Disintegrates data of digital objects of a project from additional GAMS services like solr")
@click.argument("project", required=True)
def disintegrate(project: str):
    pyrilo.disintegrate_project_objects(project)


cli.add_command(ingest)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_objects)
cli.add_command(delete_object)
cli.add_command(sync)
cli.add_command(integrate)
cli.add_command(disintegrate)


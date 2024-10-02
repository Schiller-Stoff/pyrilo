import click
import logging
from pyrilo.Pyrilo import Pyrilo

#
pyrilo =  Pyrilo("http://localhost:18085", "hsa")

@click.group()
def cli():
    """
    Pyrilo is a command line tool for managing your GAMS5 project.

    """
    logging.basicConfig( encoding='utf-8', level=logging.INFO)
    pyrilo.login()


@cli.command(name="ingest", help="Ingest bags as digital objects and datastream for a project")
@click.argument("project", required=True)
def ingest(project: str):
    pyrilo.ingest(project)
    pyrilo.integrate_project_objects(project)


@cli.command(name="create_project", help="Creates a project on GAMS")
@click.argument("project", required=True)
def create_project(project: str):
    pyrilo.create_project(project, "Demo project for testing purposes")


@cli.command(name="delete_objects", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
def delete_objects(project: str):
    pyrilo.delete_objects(project)


@click.command(name="sync", help="Syncs a project with GAMS: Deletes all objects (and performs disintegration), ingests new objects and integrates them")
@click.argument("project", required=True)
def sync(project: str):
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
cli.add_command(delete_objects)
cli.add_command(sync)
cli.add_command(integrate)
cli.add_command(disintegrate)

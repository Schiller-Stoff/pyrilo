from pathlib import Path

import click
import logging
from pyrilo.Pyrilo import Pyrilo

@click.group()
@click.option("--host", "-h", default="http://localhost:18085", help="The host of the GAMS5 instance")
@click.option("--bag_root", "-r", default=None, help="Root folder path of the bagit files. Defaults to ./bags")
@click.pass_context
def cli(ctx, host: str, bag_root: str):
    """
    Pyrilo is a command line tool for managing your GAMS5 project.

    """
    logging.basicConfig( encoding='utf-8', level=logging.INFO, force=True)

    # ensure context exists and is a dictionary
    ctx.ensure_object(dict)
    client = Pyrilo(host)
    ctx.obj['CLIENT'] = client

    if bag_root:
        # Resolve to absolute path immediately to avoid relative path confusion later
        resolved_path = str(Path(bag_root).resolve())
    else:
        # Default: The user is running this IN their project folder
        resolved_path = str(Path.cwd() / "bags")

    client.configure(host, resolved_path)
    client.login()


@cli.command(name="ingest", help="Ingest bags as digital objects and datastream for a project. Removes all digital objects and datastreams beforehand")
@click.argument("project", required=True)
@click.pass_context
def ingest(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.create_project(project, "Demo project for testing purposes")
    client.ingest_bags(project)


@cli.command(name="create_project", help="Creates a project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
@click.pass_context
def create_project(ctx, project: str, desc: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.create_project(project, desc)

@cli.command(name="update_project", help="Updates an existing project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
@click.pass_context
def update_project(ctx, project: str, desc: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.update_project(project, desc)

@cli.command(name="delete_objects", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.pass_context
def delete_objects(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.delete_objects(project)

@cli.command(name="delete_object", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.argument("object_id", required=True)
@click.pass_context
def delete_object(ctx, project:str, object_id: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.delete_object(object_id, project)

@cli.command(name="create_collection", help="Creates a collection of digital objects on the GAMS-API.")
@click.argument("project", required=True)
@click.argument("id", required=True)
@click.argument("title", required=True)
@click.argument("desc", required=False)
@click.pass_context
def create_collection(ctx, project: str, id: str, title: str, desc: str):
    """
    Creates a GAMS collection of digital objects.
    A collection must have an "owning project".
    """
    client: Pyrilo = ctx.obj['CLIENT']
    client.create_collection(project, id, title, desc)

@cli.command(name="delete_collection", help="Deletes a collection of digital objects on the GAMS-API.")
@click.argument("project", required=True)
@click.argument("id", required=True)
@click.pass_context
def delete_collection(ctx, project: str, id: str):
    """
    Deletes a GAMS collection
    """
    client: Pyrilo = ctx.obj['CLIENT']
    client.delete_collection(
        project_abbr=project,
        collection_id=id
    )

@cli.command(name="integrate", help="Integrates data of digital objects of a project with additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def integrate(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.setup_integration_services(project)
    client.integrate_project_objects(project)

@click.command(name="disintegrate", help="Disintegrates data of digital objects of a project from additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def disintegrate(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    client.disintegrate_project_objects(project)

@click.group()
def sync():
    """ Synchronization / integration commands for GAMS5 projects """
    pass

@sync.command('custom_search', help="Handles synchronization with the custom_search service")
@click.argument("project", required=True)
@click.option("--remove", "-r", default=False, help="If set, removes all data from the custom_search service", is_flag=True)
@click.pass_context
def base_search(ctx, project: str, remove: bool):
    client: Pyrilo = ctx.obj['CLIENT']
    if remove:
        client.disintegrate_project_objects_custom_search(project)
    else:
        client.integrate_project_objects_custom_search(project)

@sync.command('plexus_search', help="Handles synchronization with the plexus_search service")
@click.argument("project", required=True)
@click.option("--remove", "-r", default=False, help="If set, removes all data from the custom_search service", is_flag=True)
@click.pass_context
def plexus_search(ctx, project: str, remove: bool):
    client: Pyrilo = ctx.obj['CLIENT']
    if remove:
        client.disintegrate_project_objects_plexus_search(project)
    else:
        client.integrate_project_objects_plexus_search(project)


cli.add_command(ingest)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_objects)
cli.add_command(delete_object)
cli.add_command(integrate)
cli.add_command(disintegrate)
cli.add_command(sync)

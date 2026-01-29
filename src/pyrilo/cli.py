import sys
from pathlib import Path

import click
import logging

import requests

from pyrilo.Pyrilo import Pyrilo

# 1. Configure Logging Helper
def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        force=True
    )


@click.group()
@click.option("--host", "-h", default="http://localhost:18085", help="The host of the GAMS5 instance")
@click.option("--bag_root", "-r", default=None, help="Root folder path of the bagit files. Defaults to ./bags")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose debug logging")
@click.pass_context
def cli(ctx, host: str, bag_root: str, verbose: bool):
    """
    Pyrilo is a command line tool for managing your GAMS5 project.
    """
    setup_logging(verbose)

    ctx.ensure_object(dict)

    # Initialize Client
    try:
        client = Pyrilo(host)

        if bag_root:
            resolved_path = str(Path(bag_root).resolve())
        else:
            resolved_path = str(Path.cwd() / "bags")

        client.configure(host, resolved_path)

        # Login is the first point of failure
        client.login()

        ctx.obj['CLIENT'] = client

    except requests.exceptions.ConnectionError:
        logging.critical(f"Could not connect to GAMS host: {host}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Initialization failed: {e}")
        if verbose:
            logging.exception("Stacktrace:")
        sys.exit(1)


@cli.command(name="ingest")
@click.argument("project", required=True)
@click.pass_context
def ingest(ctx, project: str):
    """Ingest bags for a project."""
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        # We can try to create, but if it fails (e.g. exists), we might want to continue
        try:
            client.create_project(project, "Auto-created by ingest")
        except ValueError:
            logging.info(f"Project {project} already exists (or creation failed non-fatally). Continuing...")

        client.ingest_bags(project)
        logging.info("Ingest complete.")
    except Exception as e:
        logging.critical(f"Ingest failed: {e}")
        sys.exit(1)


@cli.command(name="create_project")
@click.argument("project", required=True)
@click.argument("desc", required=False, default="")
@click.pass_context
def create_project(ctx, project: str, desc: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.create_project(project, desc)
    except Exception as e:
        logging.error(f"Failed to create project: {e}")
        sys.exit(1)

@cli.command(name="update_project", help="Updates an existing project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
@click.pass_context
def update_project(ctx, project: str, desc: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.update_project(project, desc)
    except Exception as e:
        logging.error(f"Failed to update project: {e}")
        sys.exit(1)


@cli.command(name="delete_objects", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.pass_context
def delete_objects(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.delete_objects(project)
    except Exception as e:
        logging.error(f"Failed to delete objects: {e}")
        sys.exit(1)


@cli.command(name="delete_object", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.argument("object_id", required=True)
@click.pass_context
def delete_object(ctx, project:str, object_id: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.delete_object(object_id, project)
    except Exception as e:
        logging.error(f"Failed to delete object: {e}")
        sys.exit(1)

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
    try:
        client.create_collection(project, id, title, desc)
    except Exception as e:
        logging.error(f"Failed to create collection: {e}")
        sys.exit(1)


@cli.command(name="delete_collection", help="Deletes a collection of digital objects on the GAMS-API.")
@click.argument("project", required=True)
@click.argument("id", required=True)
@click.pass_context
def delete_collection(ctx, project: str, id: str):
    """
    Deletes a GAMS collection
    """
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.delete_collection(project, id)
    except Exception as e:
        logging.error(f"Failed to delete collection: {e}")
        sys.exit(1)

@cli.command(name="integrate", help="Integrates data of digital objects of a project with additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def integrate(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.setup_integration_services(project)
        client.integrate_project_objects(project)
    except Exception as e:
        logging.error(f"Failed to integrate objects: {e}")
        sys.exit(1)


@click.command(name="disintegrate", help="Disintegrates data of digital objects of a project from additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def disintegrate(ctx, project: str):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        client.disintegrate_project_objects(project)
    except Exception as e:
        logging.error(f"Failed to disintegrate objects: {e}")
        sys.exit(1)

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
    try:
        if remove:
            client.disintegrate_project_objects_custom_search(project)
        else:
            client.integrate_project_objects_custom_search(project)
    except Exception as e:
        logging.error(f"Failed to integrate objects: {e}")
        sys.exit(1)

@sync.command('plexus_search', help="Handles synchronization with the plexus_search service")
@click.argument("project", required=True)
@click.option("--remove", "-r", default=False, help="If set, removes all data from the custom_search service", is_flag=True)
@click.pass_context
def plexus_search(ctx, project: str, remove: bool):
    client: Pyrilo = ctx.obj['CLIENT']
    try:
        if remove:
            client.disintegrate_project_objects_plexus_search(project)
        else:
            client.integrate_project_objects_plexus_search(project)
    except Exception as e:
        logging.error(f"Failed to integrate objects: {e}")
        sys.exit(1)

cli.add_command(ingest)
cli.add_command(create_project)
cli.add_command(update_project)
cli.add_command(delete_objects)
cli.add_command(delete_object)
cli.add_command(integrate)
cli.add_command(disintegrate)
cli.add_command(sync)

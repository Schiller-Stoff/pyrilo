import sys
import os
from pathlib import Path

import click
import logging
import requests

from pyrilo.Pyrilo import Pyrilo
from pyrilo.api.DigitalObject.DigitalObjectService import DigitalObjectService
from pyrilo.api.GamsApiClient import GamsApiClient
from pyrilo.api.IngestService import IngestService
from pyrilo.api.IntegrationService import IntegrationService
from pyrilo.api.Project.exceptions import ProjectAlreadyExistsError
from pyrilo.api.Project.ProjectService import ProjectService
from pyrilo.api.auth.AuthorizationService import AuthorizationService


# 1. Configure Logging Helper
def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        force=True
    )


def bootstrap_application(host: str, bag_root: str) -> Pyrilo:
    """
    The Composition Root.
    Constructs the object graph and returns the fully assembled application.
    """
    # 1. Infrastructure / Core Clients
    # Resolve the path here, not deep inside the service
    if bag_root:
        resolved_bag_path = str(Path(bag_root).resolve())
    else:
        resolved_bag_path = str(Path.cwd() / "bags")

    client = GamsApiClient(host)

    # 2. Services (Injecting the client)
    auth_service = AuthorizationService(client)
    digital_object_service = DigitalObjectService(client)

    # IngestService needs both client and the file path
    ingest_service = IngestService(client, local_bagit_files_path=resolved_bag_path)

    integration_service = IntegrationService(client)
    project_service = ProjectService(client)

    # 3. Facade (Injecting the services)
    app = Pyrilo(
        bag_root,
        authorization_service=auth_service,
        digital_object_service=digital_object_service,
        ingest_service=ingest_service,
        integration_service=integration_service,
        project_service=project_service
    )

    return app

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

    # Initialize pyrilo-app
    try:
        pyrilo_app = bootstrap_application(host, bag_root)

        # Handle Credentials at the CLI/Entrypoint layer
        # 1. Try Environment Variables first (Best for CI/CD/Docker)
        username = os.environ.get("PYRILO_USER")
        password = os.environ.get("PYRILO_PASSWORD")

        # 2. If not found, prompt the user interactively
        if not username or not password:
            click.echo(f"Authentication required for {host}")
            if not username:
                username = click.prompt("Username")
            if not password:
                password = click.prompt("Password", hide_input=True)

        # 3. Pass credentials to the service
        pyrilo_app.login(username, password)

        ctx.obj['PYRILO_APP'] = pyrilo_app

    except requests.exceptions.ConnectionError:
        logging.critical(f"Could not connect to GAMS host: {host}")
        sys.exit(1)
    except ValueError as e:
        logging.critical(f"Configuration/Auth Error: {e}")
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
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        # We can try to create, but if it fails (e.g. exists), we might want to continue
        try:
            pyrilo_app.create_project(project, "Auto-created by ingest")
        except ProjectAlreadyExistsError:
            logging.info(f"Project {project} already exists (or creation failed non-fatally). Continuing...")

        pyrilo_app.ingest_bags(project)
        logging.info("Ingest complete.")
    except Exception as e:
        logging.critical(f"Ingest failed: {e}")
        sys.exit(1)


@cli.command(name="create_project")
@click.argument("project", required=True)
@click.argument("desc", required=False, default="")
@click.pass_context
def create_project(ctx, project: str, desc: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.create_project(project, desc)
        logging.info(f"Successfully created project: {project}")
    except Exception as e:
        logging.error(f"Failed to create project: {e}")
        sys.exit(1)

@cli.command(name="update_project", help="Updates an existing project on GAMS")
@click.argument("project", required=True)
@click.argument("desc", required=False)
@click.pass_context
def update_project(ctx, project: str, desc: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.update_project(project, desc)
    except Exception as e:
        logging.error(f"Failed to update project: {e}")
        sys.exit(1)


@cli.command(name="delete_objects", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.pass_context
def delete_objects(ctx, project: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.delete_objects(project)
    except Exception as e:
        logging.error(f"Failed to delete objects: {e}")
        sys.exit(1)


@cli.command(name="delete_object", help="Deletes all objects of a project on GAMS")
@click.argument("project", required=True)
@click.argument("object_id", required=True)
@click.pass_context
def delete_object(ctx, project:str, object_id: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.delete_object(object_id, project)
    except Exception as e:
        logging.error(f"Failed to delete object: {e}")
        sys.exit(1)

@cli.command(name="integrate", help="Integrates data of digital objects of a project with additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def integrate(ctx, project: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.setup_integration_services(project)
        pyrilo_app.integrate_project_objects(project)
    except Exception as e:
        logging.error(f"Failed to integrate objects: {e}")
        sys.exit(1)


@click.command(name="disintegrate", help="Disintegrates data of digital objects of a project from additional GAMS services like solr")
@click.argument("project", required=True)
@click.pass_context
def disintegrate(ctx, project: str):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        pyrilo_app.disintegrate_project_objects(project)
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
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        if remove:
            pyrilo_app.disintegrate_project_objects_custom_search(project)
        else:
            pyrilo_app.integrate_project_objects_custom_search(project)
    except Exception as e:
        logging.error(f"Failed to integrate objects: {e}")
        sys.exit(1)

@sync.command('plexus_search', help="Handles synchronization with the plexus_search service")
@click.argument("project", required=True)
@click.option("--remove", "-r", default=False, help="If set, removes all data from the custom_search service", is_flag=True)
@click.pass_context
def plexus_search(ctx, project: str, remove: bool):
    pyrilo_app: Pyrilo = ctx.obj['PYRILO_APP']
    try:
        if remove:
            pyrilo_app.disintegrate_project_objects_plexus_search(project)
        else:
            pyrilo_app.integrate_project_objects_plexus_search(project)
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
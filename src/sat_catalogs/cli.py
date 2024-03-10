"""Main entry point"""

import bz2
import os

import click
from requests import get

from .functions.dolibarr import get_dolibarr_function
from .functions.erpnext import get_erpnext_function
from .functions.odoo import get_odoo_function
from .orm import SatModel


@click.group()
@click.pass_context
def cli(context: click.Context):
    """Simple CLI tool to manage SAT's catalog SQL scripts"""
    templates_path = os.path.dirname(__file__)
    context.obj = {
        "templates_path": templates_path + "/templates",
    }


@cli.command()
@click.argument(
    "database", type=click.Path(exists=True, readable=True, resolve_path=True)
)
@click.argument("system", type=click.Choice(["dolibarr", "odoo", "erpnext"]))
@click.option(
    "-m",
    "--model",
    "model",
    required=True,
    type=click.Choice([model.name for model in SatModel], case_sensitive=False),
    help="Database object model to export",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    help="Output file",
)
@click.pass_context
def export(context: click.Context, database: str, system: str, model: str, output: str):
    """Exports data script for ERP modules

    DATABASE: SQLite database file.\n
    SYSTEM: ERP System where script is going to be used
    """
    functions_map = {
        "dolibarr": get_dolibarr_function,
        "odoo": get_odoo_function,
        "erpnext": get_erpnext_function,
    }
    get_data_function = functions_map[system](SatModel[model])
    sql = get_data_function(  # pylint: disable=not-callable
        database, context.obj["templates_path"]
    )

    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(sql)
    else:
        click.echo(f"response: {sql}")


@cli.command()
@click.option(
    "-n",
    "--name",
    "db_path",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True),
    default="catalogs.db",
    show_default=True,
    help="Name or path to build the database",
)
@click.option(
    "-o",
    "--overwrite",
    "overwrite",
    is_flag=True,
    default=False,
    show_default=True,
    help="Allow overwriting database file",
)
def build_database(db_path: str, overwrite: bool):
    """Download and build latest SAT's catalogs database"""

    if os.path.exists(db_path) and not overwrite:
        msg = (
            f"Database file {db_path} already exists. "
            "If you want to overwrite it use the --overwrite option."
        )
        raise click.ClickException(msg)

    click.echo("⇩ Downloading file...")
    url = (
        "https://github.com/phpcfdi/resources-sat-catalogs/releases/latest/download/"
        "catalogs.db.bz2"
    )
    request = get(url, timeout=60)

    click.echo("📦 Extracting database...")
    db = bz2.decompress(request.content)

    if os.path.exists(db_path) and overwrite:
        os.unlink(db_path)

    with open(db_path, "wb") as file:
        file.write(db)

    click.echo(f"✔ Done! Database file saved at {db_path}")

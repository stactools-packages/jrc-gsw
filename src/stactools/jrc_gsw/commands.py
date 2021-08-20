import os
import click
import logging

from stactools.jrc_gsw import stac
from stactools.jrc_gsw.collections import (
    AGGREGATED,
    MONTHLY_HISTORY,
    MONTHLY_RECURRENCE,
    ROOT,
    YEARLY_CLASSIFICATION,
)

logger = logging.getLogger(__name__)


def create_jrc_gsw_command(cli):
    """Creates the joint research centre - global surface water command line utility."""

    @cli.group(
        "jrc-gsw",
        short_help=("Commands for working with JRC-GSW data."),
    )
    def jrc_gsw():
        pass

    @jrc_gsw.command(
        "create-collection",
        short_help="Creates STAC collections for JRC-GSW data.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the root STAC Collection json.",
    )
    def create_collection_command(destination: str):
        """Creates a STAC Collection for each mapped dataset from the European Commission
        Joint Research Centre - Global Surface Water program.

        Args:
            destination (str): Directory used to store the root STAC collection.
        Returns:
            Callable
        """
        root_col = stac.create_collection(ROOT)

        for collection in [
            AGGREGATED,
            MONTHLY_HISTORY,
            MONTHLY_RECURRENCE,
            YEARLY_CLASSIFICATION,
        ]:
            col = stac.create_collection(collection)
            col.normalize_hrefs(destination)
            col.save()
            col.validate()
            root_col.add_child(col)

        root_col.normalize_hrefs(destination)
        root_col.save()
        root_col.validate()

    @jrc_gsw.command(
        "create-item",
        short_help="Create a STAC item from a given COG.",
    )
    @click.option(
        "-d",
        "--destination",
        required=True,
        help="The output directory for the STAC json.",
    )
    @click.option(
        "-s",
        "--source",
        required=True,
        help="The path to the COG.",
    )
    def create_item_command(destination: str, source: str):
        """Creates a STAC Item

        Args:
            destination (str): The output directory for the STAC json.
            source (str): The root data directory. Must follow the
                          structure found in:
                          http://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GSWE/
        """
        item = stac.create_item(source)
        item_path = os.path.join(destination, f"{item.id}.json")
        item.set_self_href(item_path)
        item.save_object()
        item.validate()

    return jrc_gsw

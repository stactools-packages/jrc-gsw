import os
from datetime import datetime
import pytz
import logging

import rasterio as rio
from shapely.geometry import box, mapping, shape

import pystac
from pystac.asset import Asset
from pystac.extensions.scientific import ScientificExtension
from stactools.jrc_gsw.constants import (CORE_JSC_GSW, JRC_GSW_PROVIDER,
                                         OCCURRENCE, CHANGE, SEASONALITY,
                                         RECURRENCE, TRANSITIONS, EXTENT)

logger = logging.getLogger(__name__)


def create_item(tif_href: str) -> pystac.Item:
    """Creates a STAC item for a JRC-GSW dataset.

    Args:
        tif_href (str): Path to input tif.

    Returns:
        pystac.Item: STAC Item object.
    """

    with rio.open(tif_href) as f:
        bounds = f.bounds

    item_id = os.path.basename(tif_href).replace('.tif', '')
    dataset_group = item_id.split("_")[0]
    geom = mapping(box(bounds.left, bounds.bottom, bounds.right, bounds.top))
    bbox = shape(geom).bounds

    metadata_datasets = {}
    metadata_datasets['occurrence'] = OCCURRENCE
    metadata_datasets['change'] = CHANGE
    metadata_datasets['seasonality'] = SEASONALITY
    metadata_datasets['recurrence'] = RECURRENCE
    metadata_datasets['transitions'] = TRANSITIONS
    metadata_datasets['extent'] = EXTENT

    metadata = metadata_datasets.get(dataset_group)

    # Datetime in UTC
    utc = pytz.utc
    start_datetime = utc.localize(
        datetime.strptime(metadata.get("START_TIME"), "%d/%m/%Y"))
    end_datetime = utc.localize(
        datetime.strptime(metadata.get("END_TIME"), "%d/%m/%Y"))

    # Create item
    item = pystac.Item(id=item_id,
                       geometry=geom,
                       bbox=bbox,
                       datetime=None,
                       properties={
                           'start_datetime': start_datetime,
                           'end_datetime': end_datetime,
                       })

    item.common_metadata.title = f"jrc-gsw-{dataset_group}"
    item.common_metadata.description = (
        "Joint Research Centre - Global Surface Water "
        f"in 10x10 degree tiles. This item is for the {dataset_group} data.")
    item.common_metadata.start_datetime = start_datetime
    item.common_metadata.end_datetime = end_datetime
    item.common_metadata.providers = [JRC_GSW_PROVIDER]

    scientific = ScientificExtension.ext(item, add_if_missing=True)
    scientific.doi = CORE_JSC_GSW.get("DOI")
    scientific.citation = CORE_JSC_GSW.get("CITATION")

    item.add_asset(
        "data",
        pystac.Asset(
            href=tif_href,
            media_type=pystac.MediaType.COG,
            roles=["data"],
            title="JRC GSW Cloud Optimized Geotiff",
        ),
    )

    return item


def create_collection(metadata: dict) -> pystac.Collection:
    """Create a STAC collection for a European Commission
    Joint Research Centre - Global Surface Water dataset.

    Args:
        metadata (dict): metadata from constants.py

    Returns:
        pystac.Collection: pystac collection object
    """

    utc = pytz.utc
    start_datetime = utc.localize(
        datetime.strptime(metadata.get("START_TIME"), "%d/%m/%Y"))
    end_datetime = utc.localize(
        datetime.strptime(metadata.get("END_TIME"), "%d/%m/%Y"))
    bbox = box(*metadata.get("SPATIAL_EXTENT")).bounds

    collection = pystac.Collection(
        id=metadata.get("ID"),
        title=metadata.get("TITLE"),
        description=metadata.get("DESCRIPTION"),
        providers=CORE_JSC_GSW.get("PROVIDERS"),
        license=CORE_JSC_GSW.get("LICENSE"),
        extent=pystac.Extent(
            pystac.SpatialExtent([bbox]),
            pystac.TemporalExtent([start_datetime, end_datetime])),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )

    scientific = ScientificExtension.ext(collection, add_if_missing=True)
    scientific.doi = CORE_JSC_GSW.get("DOI")
    scientific.citation = CORE_JSC_GSW.get("CITATION")

    collection.add_asset(
        "metadata",
        Asset(
            href=(
                "https://storage.cloud.google.com/global-surface-water/downloads_ancillary/DataUsersGuidev2020.pdf"  # noqa
            ),
            title="User Guide",
            description=(
                "Data user guide and description of the JRC GSW datasets."),
            media_type="application/pdf",
            roles=["metadata"]))

    return collection

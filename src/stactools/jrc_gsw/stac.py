from typing import Optional
import re
from pystac.common_metadata import CommonMetadata
from pystac.extensions.item_assets import ItemAssetsExtension
import logging

import rasterio as rio
from shapely.geometry import box, mapping, shape
import pystac
from pystac.asset import Asset
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
from stactools.core.io import ReadHrefModifier
from stactools.core.projection import reproject_geom
from stactools.jrc_gsw.assets import (
    ITEM_ASSETS,
    CHANGE_KEY,
    EXTENT_KEY,
    OCCURRENCE_KEY,
    RECURRENCE_KEY,
    SEASONALITY_KEY,
    TRANSITIONS_KEY,
)

from stactools.jrc_gsw.constants import (
    CITATION,
    COLLECTION_DESCRIPTION,
    COLLECTION_ID,
    COLLECTION_TITLE,
    DOI,
    END_TIME,
    EPSG,
    ID_REGEX,
    JRC_GSW_PROVIDER,
    LICENSE,
    SEASONALITY_START_TIME,
    SPATIAL_EXTENT,
    START_TIME,
)

logger = logging.getLogger(__name__)


class UnexpectedPathError(Exception):
    pass


def create_item(
    change_href: str,
    extent_href: str,
    occurrence_href: str,
    recurrence_href: str,
    seasonality_href: str,
    transitions_href: str,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for a JRC-GSW dataset.

    Returns:
        pystac.Item: STAC Item object.
    """
    if not read_href_modifier:
        read_href_modifier = lambda x: x

    # Gather information from one of the tiffs as they are
    # all the same.
    with rio.open(read_href_modifier(change_href)) as ds:
        image_shape = list(ds.shape)
        original_bbox = list(ds.bounds)
        transform = list(ds.transform)
        geom = reproject_geom(
            ds.crs, "epsg:4326", mapping(box(*ds.bounds)), precision=6
        )

    # Get ID, e.g. 0E_40Nv1_3_2020
    m = re.match(ID_REGEX, change_href)
    if not m:
        raise UnexpectedPathError(
            f"{change_href} does not fit stactool's expected format"
        )

    item_id = m.group(1)
    bbox = list(shape(geom).bounds)

    start_datetime = START_TIME
    end_datetime = END_TIME

    # Create item
    item = pystac.Item(
        id=item_id,
        geometry=geom,
        bbox=bbox,
        datetime=None,
        properties={
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
        },
    )

    item.common_metadata.start_datetime = START_TIME
    item.common_metadata.end_datetime = END_TIME

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = EPSG
    projection.bbox = original_bbox
    projection.shape = image_shape
    projection.transform = transform[:6]

    scientific = ScientificExtension.ext(item, add_if_missing=True)
    scientific.doi = DOI
    scientific.citation = CITATION

    for key, href in [
        (SEASONALITY_KEY, seasonality_href),
        (OCCURRENCE_KEY, occurrence_href),
        (CHANGE_KEY, change_href),
        (RECURRENCE_KEY, recurrence_href),
        (TRANSITIONS_KEY, transitions_href),
        (EXTENT_KEY, extent_href),
    ]:
        item.add_asset(key, ITEM_ASSETS[key].create_asset(href))

    # Set start time on seasonality as it is different from others
    seasonality_common_metadata = CommonMetadata(item.assets[SEASONALITY_KEY])
    seasonality_common_metadata.start_datetime = SEASONALITY_START_TIME
    # JSON validation Requires that we also set end time
    seasonality_common_metadata.end_datetime = END_TIME

    return item


def create_collection() -> pystac.Collection:
    """Create a STAC collection for a European Commission
    Joint Research Centre - Global Surface Water dataset.

    Args:
        metadata (dict): metadata from constants.py

    Returns:
        pystac.Collection: pystac collection object
    """

    collection = pystac.Collection(
        id=COLLECTION_ID,
        title=COLLECTION_TITLE,
        description=COLLECTION_DESCRIPTION,
        providers=[JRC_GSW_PROVIDER],
        license=LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent([SPATIAL_EXTENT]),
            pystac.TemporalExtent([START_TIME, END_TIME]),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )

    scientific = ScientificExtension.ext(collection, add_if_missing=True)
    scientific.doi = DOI
    scientific.citation = CITATION

    item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
    item_assets.item_assets = ITEM_ASSETS

    collection.add_asset(
        "guide",
        Asset(
            href=(
                "https://storage.cloud.google.com/global-surface-water/downloads_ancillary/DataUsersGuidev2020.pdf"  # noqa
            ),
            title="User Guide",
            description=("Data user guide and description of the JRC GSW datasets."),
            media_type="application/pdf",
            roles=["metadata"],
        ),
    )

    return collection

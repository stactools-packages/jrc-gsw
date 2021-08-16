from dateutil.relativedelta import relativedelta
from typing import Optional
from os import path

import logging

import rasterio as rio
from shapely.geometry import box, mapping, shape
import pystac
from pystac.asset import Asset
from pystac.common_metadata import CommonMetadata
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.version import ItemVersionExtension
from pystac.utils import str_to_datetime
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
    MONTHLY_HISTORY_KEY,
    MONTHLY_RECURRENCE_KEY,
    MONTHLY_RECURRENCE_OBSERVATIONS_KEY,
    YEARLY_CLASSIFICATION_KEY,
)

from stactools.jrc_gsw.constants import (
    CITATION,
    COLLECTION_DESCRIPTION,
    COLLECTION_ID,
    COLLECTION_TITLE,
    DOWNLOAD_VERSION,
    DOI,
    END_TIME,
    EPSG,
    JRC_GSW_PROVIDER,
    LATEST_VERSION,
    LICENSE,
    SEASONALITY_START_TIME,
    SPATIAL_EXTENT,
    START_TIME,
)

logger = logging.getLogger(__name__)


class UnexpectedPathError(Exception):
    pass


def create_item(
    source: str,
    tile_id: str,
    year: int,
    month: int,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for a JRC-GSW dataset.

    Returns:
        pystac.Item: STAC Item object.
    """

    if not read_href_modifier:
        read_href_modifier = lambda x: x

    agg_types = [
        "change",
        "extent",
        "occurrence",
        "recurrence",
        "seasonality",
        "transitions",
    ]

    agg_hrefs = {}
    for agg_type in agg_types:
        agg_hrefs[agg_type] = path.join(
            source,
            f"Aggregated/{DOWNLOAD_VERSION}/{agg_type}/tiles/{agg_type}-{tile_id}.tif",
        )  # noqa

    # Gather information from one of the tiffs as they are
    # all the same.
    with rio.open(read_href_modifier(agg_hrefs["change"])) as ds:
        image_shape = list(ds.shape)
        original_bbox = list(ds.bounds)
        transform = list(ds.transform)
        geom = reproject_geom(
            ds.crs, "epsg:4326", mapping(box(*ds.bounds)), precision=6
        )

    month_zfill = str(month).zfill(2)

    item_id = f"{tile_id}_{year}_{month_zfill}"
    bbox = list(shape(geom).bounds)

    start_datetime = str_to_datetime(f"{year}-{month_zfill}-01T00:00:00Z")
    end_datetime = start_datetime + relativedelta(months=1)

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

    item.common_metadata.start_datetime = start_datetime
    item.common_metadata.end_datetime = end_datetime

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = EPSG
    projection.bbox = original_bbox
    projection.shape = image_shape
    projection.transform = transform[:6]

    scientific = ScientificExtension.ext(item, add_if_missing=True)
    scientific.doi = DOI
    scientific.citation = CITATION

    version = ItemVersionExtension.ext(item, add_if_missing=True)
    version.version = LATEST_VERSION

    # Create Aggregation assets
    for key, href in [
        (SEASONALITY_KEY, agg_hrefs["seasonality"]),
        (OCCURRENCE_KEY, agg_hrefs["occurrence"]),
        (CHANGE_KEY, agg_hrefs["change"]),
        (RECURRENCE_KEY, agg_hrefs["recurrence"]),
        (TRANSITIONS_KEY, agg_hrefs["transitions"]),
        (EXTENT_KEY, agg_hrefs["extent"]),
    ]:
        item.add_asset(key, ITEM_ASSETS[key].create_asset(href))

    # Set start time on seasonality as it is different from others
    seasonality_common_metadata = CommonMetadata(item.assets[SEASONALITY_KEY])
    seasonality_common_metadata.start_datetime = SEASONALITY_START_TIME
    # JSON validation Requires that we also set end time
    seasonality_common_metadata.end_datetime = END_TIME

    # Create Monthly History asset
    monthly_history_root = f"{source}/MonthlyHistory/{DOWNLOAD_VERSION}/tiles"
    monthly_history_href = f"{monthly_history_root}/{year}/{year}_{month_zfill}/{year}_{month_zfill}-{tile_id}.tif"  # noqa
    item.add_asset(
        MONTHLY_HISTORY_KEY,
        ITEM_ASSETS[MONTHLY_HISTORY_KEY].create_asset(monthly_history_href),
    )

    # Create Monthly Recurrence assets
    monthly_recurrence_root = f"{source}/MonthlyRecurrence/{DOWNLOAD_VERSION}/tiles"
    monthly_recurrence_href = (
        f"{monthly_recurrence_root}/monthlyRecurrence{month}/{tile_id}.tif"  # noqa
    )
    item.add_asset(
        MONTHLY_RECURRENCE_KEY,
        ITEM_ASSETS[MONTHLY_RECURRENCE_KEY].create_asset(monthly_recurrence_href),
    )

    monthly_recurrence_observations_href = (
        f"{monthly_recurrence_root}/has_observations{month}/{tile_id}.tif"  # noqa
    )
    item.add_asset(
        MONTHLY_RECURRENCE_OBSERVATIONS_KEY,
        ITEM_ASSETS[MONTHLY_RECURRENCE_OBSERVATIONS_KEY].create_asset(
            monthly_recurrence_observations_href
        ),
    )

    # Create Yearly Classification asset
    yearly_classification_href = f"{source}/YearlyClassification/{DOWNLOAD_VERSION}/tiles/yearlyClassification{year}/yearlyClassification{year}-{tile_id}.tif"  # noqa
    item.add_asset(
        YEARLY_CLASSIFICATION_KEY,
        ITEM_ASSETS[YEARLY_CLASSIFICATION_KEY].create_asset(yearly_classification_href),
    )

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
            description=("Data users guide and description of the JRC GSW datasets."),
            media_type="application/pdf",
            roles=["metadata"],
        ),
    )

    return collection

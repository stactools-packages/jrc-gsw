from dateutil.relativedelta import relativedelta
import os.path
from typing import Optional

import logging

import rasterio as rio
from shapely.geometry import box, mapping, shape

import pystac
from pystac.asset import Asset
from pystac.extensions.item_assets import ItemAssetsExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.version import ItemVersionExtension
from pystac.utils import str_to_datetime, datetime_to_str

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
    YEARLY_CLASSIFICATION_KEY,
)
from stactools.jrc_gsw.collections import (
    AGGREGATED,
    MONTHLY_HISTORY,
    MONTHLY_RECURRENCE,
    YEARLY_CLASSIFICATION,
)

from stactools.jrc_gsw.constants import (
    CITATION,
    DOWNLOAD_VERSION,
    DOI,
    END_TIME,
    EPSG,
    JRC_GSW_PROVIDER,
    LATEST_VERSION,
    LICENSE,
    START_TIME,
)

logger = logging.getLogger(__name__)


class UnexpectedPathError(Exception):
    pass


def create_item(
    source: str,
    read_href_modifier: Optional[ReadHrefModifier] = None,
) -> pystac.Item:
    """Creates a STAC item for a JRC-GSW dataset.

    Args:
        source (str): path to COG

    Returns:
        pystac.Item: STAC Item object.
    """

    if not read_href_modifier:
        read_href_modifier = lambda x: x

    collection_name = os.path.basename(
        os.path.dirname(source.split(DOWNLOAD_VERSION)[0])
    )

    item_id = os.path.splitext("-".join(os.path.basename(source).split("-")[-2:]))[0]

    root_path = os.path.dirname(source.split(collection_name)[0])

    with rio.open(read_href_modifier(source)) as ds:
        image_shape = list(ds.shape)
        original_bbox = list(ds.bounds)
        transform = list(ds.transform)
        geometry = reproject_geom(
            ds.crs, "epsg:4326", mapping(box(*ds.bounds)), precision=6
        )
        bbox = list(shape(geometry).bounds)

    assets = {}

    if collection_name == "Aggregated":
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
            agg_hrefs[
                agg_type
            ] = f"{root_path}/Aggregated/{DOWNLOAD_VERSION}/{agg_type}/tiles/{agg_type}-{item_id}.tif"  # noqa

        start_datetime = START_TIME
        end_datetime = END_TIME
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        for key, href in [
            (SEASONALITY_KEY, agg_hrefs["seasonality"]),
            (OCCURRENCE_KEY, agg_hrefs["occurrence"]),
            (CHANGE_KEY, agg_hrefs["change"]),
            (RECURRENCE_KEY, agg_hrefs["recurrence"]),
            (TRANSITIONS_KEY, agg_hrefs["transitions"]),
            (EXTENT_KEY, agg_hrefs["extent"]),
        ]:
            assets[key] = ITEM_ASSETS[AGGREGATED["ID"]][key].create_asset(href)

    elif collection_name == "MonthlyHistory":
        year_month = os.path.basename(source).split("-")[0].split("_")
        year = year_month[0]
        month = year_month[1]

        start_datetime = str_to_datetime(f"{year}-{month}-01T00:00:00Z")
        end_datetime = start_datetime + relativedelta(months=1)
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        assets[MONTHLY_HISTORY_KEY] = ITEM_ASSETS[MONTHLY_HISTORY["ID"]][
            MONTHLY_HISTORY_KEY
        ].create_asset(source)

    elif collection_name == "MonthlyRecurrence":
        month = os.path.dirname(source.split("monthlyRecurrence")[1])

        start_datetime = START_TIME
        end_datetime = END_TIME
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        if "monthlyRecurrence" in source:
            parent_dir = os.path.dirname(source.split("monthlyRecurrence")[0])
        else:
            parent_dir = os.path.dirname(source.split("has_observations")[0])

        asset_types = ["monthlyRecurrence", "has_observations"]

        for i in range(12):
            for asset_type in asset_types:
                asset_key = f"{asset_type}{i+1}"
                href = os.path.join(parent_dir, asset_key, f"{item_id}.tif")
                assets[asset_key] = ITEM_ASSETS[MONTHLY_RECURRENCE["ID"]][
                    asset_key
                ].create_asset(href)

    elif collection_name == "YearlyClassification":
        year = os.path.dirname(source.split("yearlyClassification")[1])

        start_datetime = str_to_datetime(f"{year}-01-01T00:00:00Z")
        end_datetime = start_datetime + relativedelta(years=1)
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        assets[YEARLY_CLASSIFICATION_KEY] = ITEM_ASSETS[YEARLY_CLASSIFICATION["ID"]][
            YEARLY_CLASSIFICATION_KEY
        ].create_asset(source)

    item = pystac.Item(
        id=item_id,
        geometry=geometry,
        bbox=bbox,
        datetime=None,
        properties=properties,
    )

    for k, v in assets.items():
        item.add_asset(k, v)

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

    return item


def create_collection(collection_defn: dict) -> pystac.Collection:
    """Create a STAC collection for a European Commission
    Joint Research Centre - Global Surface Water dataset.

    Args:
        collection_defn (dict): metadata from collections.py

    Returns:
        pystac.Collection: pystac collection object
    """

    collection = pystac.Collection(
        id=collection_defn["ID"],
        title=collection_defn["TITLE"],
        description=collection_defn["DESCRIPTION"],
        providers=[JRC_GSW_PROVIDER],
        license=LICENSE,
        extent=pystac.Extent(
            pystac.SpatialExtent([collection_defn["SPATIAL_EXTENT"]]),
            pystac.TemporalExtent(
                [collection_defn["START_TIME"], collection_defn["END_TIME"]]
            ),
        ),
        catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED,
    )

    scientific = ScientificExtension.ext(collection, add_if_missing=True)
    scientific.doi = DOI
    scientific.citation = CITATION

    assets = ITEM_ASSETS.get(collection_defn["ID"])
    if assets is not None:
        item_assets = ItemAssetsExtension.ext(collection, add_if_missing=True)
        item_assets.item_assets = assets

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

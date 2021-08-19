import fsspec
import logging
import os.path

from dateutil.relativedelta import relativedelta
from typing import Optional

import rasterio as rio
from shapely.geometry import box, mapping, shape

import pystac
from pystac.asset import Asset
from pystac.extensions.file import FileExtension
from pystac.extensions.item_assets import AssetDefinition, ItemAssetsExtension
from pystac.extensions.scientific import ScientificExtension
from pystac.extensions.projection import ProjectionExtension
from pystac.extensions.raster import RasterBand, RasterExtension
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


def collect_raster_stats(href: str) -> dict:
    raster_stats = {}
    with rio.open(href) as ds:
        raster_stats["shape"] = list(ds.shape)
        raster_stats["transform"] = list(ds.transform)
        raster_stats["geometry"] = reproject_geom(
            ds.crs, "epsg:4326", mapping(box(*ds.bounds)), precision=6
        )
        raster_stats["proj_bbox"] = list(shape(raster_stats["geometry"]).bounds)
        raster_stats["orig_bbox"] = list(ds.bounds)

        raster_bands = []
        for i in range(ds.count):
            raster_bands.append(
                RasterBand.create(
                    data_type=ds.dtypes[i],
                    sampling=ds.tags().get("AREA_OR_POINT").lower(),
                )
            )
        raster_stats["bands"] = raster_bands

    with fsspec.open(href) as file:
        size = file.size
        if size is not None:
            raster_stats["size"] = size

    return raster_stats


def assemble_asset(asset_defn: AssetDefinition, href: str) -> dict:
    raster_stats = collect_raster_stats(href)

    return {
        "asset_defn": asset_defn.create_asset(href),
        "raster_stats": raster_stats,
    }


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
            assets[key] = assemble_asset(ITEM_ASSETS[AGGREGATED["ID"]][key], href)

    elif collection_name == "MonthlyHistory":
        year_month = os.path.basename(source).split("-")[0].split("_")
        year = year_month[0]
        month = year_month[1]

        item_id += f"_{year}_{month}"

        start_datetime = str_to_datetime(f"{year}-{month}-01T00:00:00Z")
        end_datetime = start_datetime + relativedelta(months=1)
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        assets[MONTHLY_HISTORY_KEY] = assemble_asset(
            ITEM_ASSETS[MONTHLY_HISTORY["ID"]][MONTHLY_HISTORY_KEY], source
        )

    elif collection_name == "MonthlyRecurrence":
        month = os.path.dirname(source.split("monthlyRecurrence")[1])
        item_id += f"_{str(month).zfill(2)}"

        start_datetime = START_TIME
        end_datetime = END_TIME
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        if "monthlyRecurrence" in source:
            recurrence_href = source
            observations_href = source.replace("monthlyRecurrence", "has_observations")
        else:
            observations_href = source
            recurrence_href = source.replace("has_observations", "monthlyRecurrence")

        asset_types = {
            "monthlyRecurrence": recurrence_href,
            "has_observations": observations_href,
        }

        for k, v in asset_types.items():
            assets[k] = assemble_asset(ITEM_ASSETS[MONTHLY_RECURRENCE["ID"]][k], v)

    elif collection_name == "YearlyClassification":
        year = os.path.dirname(source.split("yearlyClassification")[1])
        item_id += f"_{year}"

        start_datetime = str_to_datetime(f"{year}-01-01T00:00:00Z")
        end_datetime = start_datetime + relativedelta(years=1)
        properties = {
            "start_datetime": datetime_to_str(start_datetime),
            "end_datetime": datetime_to_str(end_datetime),
        }

        assets[YEARLY_CLASSIFICATION_KEY] = assemble_asset(
            ITEM_ASSETS[YEARLY_CLASSIFICATION["ID"]][YEARLY_CLASSIFICATION_KEY], source
        )

    first_asset_key = list(assets.keys())[0]
    raster_stats = assets[first_asset_key]["raster_stats"]

    item = pystac.Item(
        id=item_id,
        geometry=raster_stats["geometry"],
        bbox=raster_stats["orig_bbox"],
        datetime=None,
        properties=properties,
    )

    for k, v in assets.items():
        asset = v["asset_defn"]
        item.add_asset(k, asset)

        file_ext = FileExtension.ext(asset, add_if_missing=True)
        file_ext.size = v["raster_stats"]["size"]

        raster = RasterExtension.ext(asset, add_if_missing=True)
        raster.bands = v["raster_stats"]["bands"]

    projection = ProjectionExtension.ext(item, add_if_missing=True)
    projection.epsg = EPSG
    projection.bbox = raster_stats["proj_bbox"]
    projection.shape = raster_stats["shape"]
    projection.transform = raster_stats["transform"][:6]

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

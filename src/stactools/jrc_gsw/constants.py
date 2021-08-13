# flake8: noqa
import re

from pyproj import CRS
import pystac
from pystac.utils import str_to_datetime

COLLECTION_ID = "jrc-gsw"
COLLECTION_TITLE = "European Commission Joint Research Centre - Global Surface Water"
COLLECTION_DESCRIPTION = "Global surface water products from the European Commission Joint Research Centre, based on Landsat 5, 7, and 8 imagery.  Layers in this collection describe the occurrence, change, and seasonality of surface water from 1984-2020."
LICENSE = "CC-BY-4.0"
SPATIAL_EXTENT = [-180.0, -56.0, 180.0, 78.0]

JRC_GSW_PROVIDER = pystac.Provider(
    name="European Commission Joint Research Centre",
    roles=[pystac.ProviderRole.PRODUCER, pystac.ProviderRole.PROCESSOR],
    url="https://global-surface-water.appspot.com/",
)

# Directory to download data from
DOWNLOAD_VERSION = "LATEST"
# Version to record in version extension
LATEST_VERSION = "VER4-0"

# The overall start and end datetime for this collection.
START_TIME = str_to_datetime("1984-03-01T00:00:00Z")
END_TIME = str_to_datetime("2020-12-31T11:59:59Z")

# The seasonality asset has a different start time
SEASONALITY_START_TIME = str_to_datetime("2020-01-01T00:00:00Z")

EPSG = 4326

DOI = "10.1038/nature20584"
CITATION = "Jean-Francois Pekel, Andrew Cottam, Noel Gorelick, Alan S. Belward, High-resolution mapping of global surface water and its long-term changes. Nature 540, 418-422 (2016)"

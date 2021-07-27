# flake8: noqa
import re

from pyproj import CRS
import pystac
from pystac.utils import str_to_datetime

COLLECTION_ID = "jrc-gsw"
COLLECTION_TITLE = "European Commission Joint Research Centre - Global Surface Water"
COLLECTION_DESCRIPTION = (
    "Collection of Global Surface Water products from the "
    "European Commission Joint Research Centre. This collection presents "
    "different surface water products between 1984-2020 from "
    "Landsat 5,7, and 8 sensors."
)
LICENSE = "CC-BY-4.0"
SPATIAL_EXTENT = [-180.0, -56.0, 180.0, 78.0]

JRC_GSW_PROVIDER = pystac.Provider(
    name="Joint Research Centre - Global Surface Water",
    roles=[pystac.ProviderRole.PRODUCER, pystac.ProviderRole.PROCESSOR],
    url="https://global-surface-water.appspot.com/",
)

# Regex to extract IDs out of file names
ID_REGEX = re.compile(r".*_(\d+E_\d+Nv\d_\d_\d+).*")

# The overall start and end datetime for this collection.
START_TIME = str_to_datetime("1984-03-01T00:00:00Z")
END_TIME = str_to_datetime("2020-12-31T11:59:59Z")

# The seasonality asset has a different start time
SEASONALITY_START_TIME = str_to_datetime("2020-01-01T00:00:00Z")

EPSG = 4326

DOI = "10.1038/nature20584"
CITATION = "Jean-Francois Pekel, Andrew Cottam, Noel Gorelick, Alan S. Belward, High-resolution mapping of global surface water and its long-term changes. Nature 540, 418-422 (2016)"

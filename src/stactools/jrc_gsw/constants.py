# flake8: noqa
import re

from pyproj import CRS
import pystac
from pystac.utils import str_to_datetime

LICENSE = "CC-BY-4.0"

JRC_GSW_PROVIDER = pystac.Provider(
    name="European Commission Joint Research Centre",
    roles=[pystac.ProviderRole.PRODUCER, pystac.ProviderRole.PROCESSOR],
    url="https://global-surface-water.appspot.com/",
)

# The overall start and end datetime for this collection.
START_TIME = str_to_datetime("1984-03-01T00:00:00Z")
END_TIME = str_to_datetime("2020-12-31T11:59:59Z")

EPSG = 4326

DOI = "10.1038/nature20584"
CITATION = "Jean-Francois Pekel, Andrew Cottam, Noel Gorelick, Alan S. Belward, High-resolution mapping of global surface water and its long-term changes. Nature 540, 418-422 (2016)"

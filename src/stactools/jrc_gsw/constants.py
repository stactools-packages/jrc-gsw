# flake8: noqa

from pyproj import CRS
from pystac import Provider

CORE_JSC_GSW = dict(
    ID='jrc-gsw',
    TITLE="European Commission Joint Research Centre - Global Surface Water",
    DESCRIPTION=
    "Collection of Global Surface Water products from the European Commission Joint Research Centre. This collection presents different surface water products between 1984-2020 from Landsat 5,7, and 8 sensors.",
    CRS=CRS.from_epsg(4326),
    DOI="10.1038/nature20584",
    CITATION=
    "Jean-Francois Pekel, Andrew Cottam, Noel Gorelick, Alan S. Belward, High-resolution mapping of global surface water and its long-term changes. Nature 540, 418-422 (2016)",
    LICENSE="CC-BY-4.0",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)

JRC_GSW_PROVIDER = Provider(
    name="Joint Research Centre - Global Surface Water",
    roles=["producer", "processor", "host"],
    url="https://global-surface-water.appspot.com/")

#
# Occurrence dataset
#
OCCURRENCE = dict(
    ID="jrc_gsw_occurrence",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Occurrence",
    DESCRIPTION=
    "The Water Occurrence shows where surface water occurred between 1984 and 2020 and providesinformation concerning overall water dynamics. This product captures both the intra and inter-annual variability and changes.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)
#
# Occurrence Change dataset
#
CHANGE = dict(
    ID="jrc_gsw_change",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Occurrence Change",
    DESCRIPTION=
    "The Occurrence Change Intensity provides information on where surface water occurrence increased, decreased or remained the same between 1984-1999 and 2000-2020 Both the direction of change and its intensity are documented.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)

#
# Seasonality dataset
#
SEASONALITY = dict(
    ID="jrc_gsw_seasonality",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Seasonality",
    DESCRIPTION=
    "The Seasonality provides information concerning the intra-annual behaviour of water surfaces for a single year (2020) and shows permanent and seasonal  water  and  the number  of  months  waterwas present.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/01/2020",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)
#
# Recurrence dataset
#
RECURRENCE = dict(
    ID="jrc_gsw_recurrence",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Recurrence",
    DESCRIPTION=
    "The Recurrence provides information concerning the inter-annual behavior of water surfaces and captures the frequency with which water returns from year to year.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)
#
# Transitions dataset
#
TRANSITIONS = dict(
    ID="jrc_gsw_transitions",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Transition",
    DESCRIPTION=
    "The Transitions provides information on the change in seasonality between the first and last years and captures changes between the three classes of not water, seasonal water, and permanent water.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)
#
# Extent dataset
#
EXTENT = dict(
    ID="jrc_gsw_extent",
    TITLE=
    "European Commission Joint Research Centre - Global Surface Water Extent",
    DESCRIPTION=
    "The Maximum Water Extent provides information on all the locations ever detected as water over a 37-year period. It is the union of all of the other datasets",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME="01/03/1984",  # Keep format in dd/mm/yyyy
    END_TIME="31/12/2020"  # Keep format in dd/mm/yyyy
)

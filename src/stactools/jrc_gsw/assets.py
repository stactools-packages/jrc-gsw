from typing import Dict
import pystac
from pystac.extensions.item_assets import AssetDefinition

SEASONALITY_KEY = "seasonality"
OCCURRENCE_KEY = "occurrence"
CHANGE_KEY = "change"
RECURRENCE_KEY = "recurrence"
TRANSITIONS_KEY = "transitions"
EXTENT_KEY = "extent"
MONTHLY_HISTORY_KEY = "monthly-history"
MONTHLY_RECURRENCE_KEY = "monthly-recurrence"
MONTHLY_RECURRENCE_OBSERVATIONS_KEY = "monthly-recurrence-observations"
YEARLY_CLASSIFICATION_KEY = "yearly-classification"

ITEM_ASSETS: Dict[str, AssetDefinition] = {
    OCCURRENCE_KEY: AssetDefinition(
        {
            "title": "Occurrence",
            "description": (
                "Frequency with which water was present from March 1984 to "
                "December 2020"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    CHANGE_KEY: AssetDefinition(
        {
            "title": "Occurrence Change Intensity",
            "description": (
                "Change in water occurrence between the two periods (1984-1999) "
                "and (2000-2020)"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    SEASONALITY_KEY: AssetDefinition(
        {
            "title": "Seasonality",
            "description": (
                "Number of months that water was present from January 2020 to "
                "December 2020"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    RECURRENCE_KEY: AssetDefinition(
        {
            "title": "Recurrence",
            "description": ("Frequency with which water returns from year to year"),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    TRANSITIONS_KEY: AssetDefinition(
        {
            "title": "Transitions",
            "description": (
                "Categorical change in surface water status from 1984 to 2020"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    EXTENT_KEY: AssetDefinition(
        {
            "title": "Maximum Water Extent",
            "description": (
                "Binary indicator of whether water was ever present (from 1984-2020)"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    MONTHLY_HISTORY_KEY: AssetDefinition(
        {
            "title": "Monthly History",
            "description": ("Historical water detection on a month-by-month basis"),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    MONTHLY_RECURRENCE_KEY: AssetDefinition(
        {
            "title": "Monthly Recurrence",
            "description": (
                "Monthly measures of the seasonality of water based on the occurrence values detected in that month over all years."  # noqa
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    MONTHLY_RECURRENCE_OBSERVATIONS_KEY: AssetDefinition(
        {
            "title": "Monthly Recurrence Observations",
            "description": (
                "Binary indicator of presence of seasonal water based on the occurrence values detected in that month over all years."  # noqa
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    YEARLY_CLASSIFICATION_KEY: AssetDefinition(
        {
            "title": "Yearly Classification",
            "description": (
                "Year-by-year classification of the seasonality of water based on the occurrence values detected throughout the year."  # noqa
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
}

from datetime import datetime
from typing import Dict
import pystac
from pystac.extensions.item_assets import AssetDefinition

from stactools.jrc_gsw.collections import (
    AGGREGATED,
    MONTHLY_HISTORY,
    MONTHLY_RECURRENCE,
    YEARLY_CLASSIFICATION,
)

SEASONALITY_KEY = "seasonality"
OCCURRENCE_KEY = "occurrence"
CHANGE_KEY = "change"
RECURRENCE_KEY = "recurrence"
TRANSITIONS_KEY = "transitions"
EXTENT_KEY = "extent"
MONTHLY_HISTORY_KEY = "monthly-history"
MONTHLY_RECURRENCE_KEY = "monthlyRecurrence"
MONTHLY_RECURRENCE_OBSERVATIONS_KEY = "has_observations"
YEARLY_CLASSIFICATION_KEY = "yearly-classification"

SEASONALITY_START_TIME = "2020-01-01T00:00:00Z"
SEASONALITY_END_TIME = "2020-12-31T11:59:59Z"


ITEM_ASSETS: Dict[str, AssetDefinition] = {
    AGGREGATED["ID"]: {
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
                "start_datetime": SEASONALITY_START_TIME,
                "end_datetime": SEASONALITY_END_TIME,
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
                    "Binary indicator of whether water was ever present (from 1984-2020)"  # noqa
                ),
                "type": pystac.MediaType.COG,
                "roles": ["data"],
            }
        ),
    },
    MONTHLY_HISTORY["ID"]: {
        MONTHLY_HISTORY_KEY: AssetDefinition(
            {
                "title": "Monthly History",
                "description": ("Historical water detection on a month-by-month basis"),
                "type": pystac.MediaType.COG,
                "roles": ["data"],
            }
        )
    },
    YEARLY_CLASSIFICATION["ID"]: {
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
    },
}

MONTHLY_RECURRENCE_ASSETS = {}
for i in range(1, 13):
    month_name = datetime.strptime(str(i), "%m").strftime("%B")
    MONTHLY_RECURRENCE_ASSETS[f"{MONTHLY_RECURRENCE_KEY}{i}"] = AssetDefinition(
        {
            "title": f"Monthly Recurrence ({month_name})",
            "description": (
                "Monthly measures of the seasonality of water based on the occurrence values detected in that month over all years."  # noqa
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    )

    MONTHLY_RECURRENCE_ASSETS[
        f"{MONTHLY_RECURRENCE_OBSERVATIONS_KEY}{i}"
    ] = AssetDefinition(
        {
            "title": f"Monthly Recurrence Observations ({month_name})",
            "description": (
                "Binary indicator of presence of seasonal water based on the occurrence values detected in that month over all years."  # noqa
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    )

ITEM_ASSETS[MONTHLY_RECURRENCE["ID"]] = MONTHLY_RECURRENCE_ASSETS

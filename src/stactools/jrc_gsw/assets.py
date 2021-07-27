from typing import Dict
import pystac
from pystac.extensions.item_assets import AssetDefinition

SEASONALITY_KEY = "seasonality"
OCCURRENCE_KEY = "occurrence"
CHANGE_KEY = "occurrence_change"
RECURRENCE_KEY = "recurrence"
TRANSITIONS_KEY = "transitions"
EXTENT_KEY = "extent"

ITEM_ASSETS: Dict[str, AssetDefinition] = {
    SEASONALITY_KEY: AssetDefinition(
        {
            "title": "Water Seasonality",
            "description": (
                "Provides information concerning the intra-annual behaviour of water "
                "surfaces for a single year (2020) and shows permanent and seasonal  "
                "water  and  the number  of  months  waterwas present."
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    OCCURRENCE_KEY: AssetDefinition(
        {
            "title": "Water Occurrence",
            "description": (
                "Shows where surface water occurred between 1984 and 2020 "
                "and provides information concerning overall water dynamics. This "
                "product captures both the intra and inter-annual "
                "variability and changes."
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    CHANGE_KEY: AssetDefinition(
        {
            "title": "Water Occurrence Change",
            "description": (
                "Provides information on where surface water occurrence increased, "
                "decreased or remained the same between 1984-1999 and 2000-2020. "
                "Both the direction of change and its intensity are documented."
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    RECURRENCE_KEY: AssetDefinition(
        {
            "title": "Water Recurrence",
            "description": (
                "Provides information concerning the inter-annual behavior of water "
                "surfaces and captures the frequency with which water returns "
                "from year to year."
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    TRANSITIONS_KEY: AssetDefinition(
        {
            "title": "Water Transitions",
            "description": (
                "Provides information on the change in seasonality between the first "
                "and last years and captures changes between the three classes of not "
                "water, seasonal water, and permanent water."
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
    EXTENT_KEY: AssetDefinition(
        {
            "title": "Maximum Water Extent",
            "description": (
                "Provides information on all the locations ever detected as water over "
                "a 37-year period. It is the union of all of the other datasets"
            ),
            "type": pystac.MediaType.COG,
            "roles": ["data"],
        }
    ),
}

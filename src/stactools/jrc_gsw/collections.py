from pystac.utils import str_to_datetime

#
# Root collection
#
ROOT = dict(
    ID="jrc_gsw",
    TITLE="European Commission Joint Research Centre - Global Surface Water",  # noqa
    DESCRIPTION="Global surface water collections (aggregated, monthly history, monthly recurrence, and yearly classification)",  # noqa
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME=str_to_datetime("1984-03-01T00:00:00Z"),
    END_TIME=str_to_datetime("2020-12-31T11:59:59Z"),
)

#
# Aggregated collection
#
AGGREGATED = dict(
    ID="jrc_gsw_aggregated",
    TITLE="European Commission Joint Research Centre - Global Surface Water (Aggregated)",  # noqa
    DESCRIPTION="Global surface water datasets (occurrence, change, seasonality, recurrence, transitions and maximum extent) aggregated over 1984 - 2020.",  # noqa
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME=str_to_datetime("1984-03-01T00:00:00Z"),
    END_TIME=str_to_datetime("2020-12-31T11:59:59Z"),
)

#
# Monthly history collection
#
MONTHLY_HISTORY = dict(
    ID="jrc_gsw_monthly_history",
    TITLE="European Commission Joint Research Centre - Global Surface Water (Monthly History)",  # noqa
    DESCRIPTION="Historical water detection on a month-by-month basis.",
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME=str_to_datetime("1984-03-01T00:00:00Z"),
    END_TIME=str_to_datetime("2020-12-31T11:59:59Z"),
)

#
# Monthly recurrence collection
#
MONTHLY_RECURRENCE = dict(
    ID="jrc_gsw_monthly_recurrence",
    TITLE="European Commission Joint Research Centre - Global Surface Water (Monthly Recurrence)",  # noqa
    DESCRIPTION="Monthly measures of the seasonality of water based on the occurrence values detected in that month over all years.",  # noqa
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME=str_to_datetime("1984-03-01T00:00:00Z"),
    END_TIME=str_to_datetime("2020-12-31T11:59:59Z"),
)

#
# Yearly classification collection
#
YEARLY_CLASSIFICATION = dict(
    ID="jrc_gsw_yearly_classification",
    TITLE="European Commission Joint Research Centre - Global Surface Water (Yearly Classification)",  # noqa
    DESCRIPTION="Year-by-year classification of the seasonality of water based on the occurrence values detected throughout the year.",  # noqa
    SPATIAL_EXTENT=(-180, -56, 180, 78),
    START_TIME=str_to_datetime("1984-03-01T00:00:00Z"),
    END_TIME=str_to_datetime("2020-12-31T11:59:59Z"),
)

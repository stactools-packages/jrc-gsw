import unittest
from dateutil.relativedelta import relativedelta

from stactools.jrc_gsw.stac import create_collection, create_item
from pystac.utils import datetime_to_str, str_to_datetime

from stactools.jrc_gsw.collections import AGGREGATED

from tests import test_data


class TestSTAC(unittest.TestCase):
    def test_create_aggregated_item(self):
        item_id = "0000360000-0000480000"
        args = {
            "source": test_data.get_path(
                f"data-files/Aggregated/LATEST/change/tiles/change-{item_id}.tif"  # noqa
            )
        }

        item = create_item(**args)

        self.assertEqual(item.id, item_id)

        agg_types = [
            "change",
            "extent",
            "occurrence",
            "recurrence",
            "seasonality",
            "transitions",
        ]

        for key, asset in item.assets.items():
            if key in agg_types:
                self.assertIn(key, asset.href)
            self.assertIn(item_id, asset.href)
        self.assertEqual(len(item.stac_extensions), 3)
        self.assertIn("version", item.properties.keys())
        item.validate()

    def test_create_monthly_history_item(self):
        item_id = "0000360000-0000480000"
        year = "1984"
        month = "04"
        args = {
            "source": test_data.get_path(
                f"data-files/MonthlyHistory/LATEST/tiles/{year}/{year}_{month}/{year}_{month}-{item_id}.tif"  # noqa
            )
        }

        item = create_item(**args)

        self.assertEqual(item.id, item_id)

        start_datetime = str_to_datetime(f"{year}-{month}-01T00:00:00Z")
        end_datetime = start_datetime + relativedelta(months=1)

        self.assertEqual(
            item.properties["start_datetime"], datetime_to_str(start_datetime)
        )
        self.assertEqual(item.properties["end_datetime"], datetime_to_str(end_datetime))

        self.assertIn("monthly-history", item.assets.keys())
        self.assertEqual(len(item.stac_extensions), 3)
        self.assertIn("version", item.properties.keys())
        item.validate()

    def test_create_monthly_recurrence_item(self):
        item_id = "0000360000-0000480000"
        month = "04"
        args = {
            "source": test_data.get_path(
                f"data-files/MonthlyRecurrence/LATEST/tiles/monthlyRecurrence{int(month)}/{item_id}.tif",  # noqa
            )
        }

        item = create_item(**args)

        self.assertEqual(item.id, item_id)

        for key, asset in item.assets.items():
            self.assertTrue("monthlyRecurrence" in key or "has_observations" in key)

        self.assertEqual(len(item.assets), 24)
        self.assertEqual(len(item.stac_extensions), 3)
        self.assertIn("version", item.properties.keys())
        item.validate()

    def test_create_yearly_classification_item(self):
        item_id = "0000360000-0000480000"
        year = 1984
        args = {
            "source": test_data.get_path(
                f"data-files/YearlyClassification/LATEST/tiles/yearlyClassification{year}/yearlyClassification{year}-{item_id}.tif"  # noqa
            )
        }

        item = create_item(**args)

        self.assertEqual(item.id, item_id)

        self.assertEqual(len(item.assets), 1)
        self.assertEqual(len(item.stac_extensions), 3)
        self.assertIn("version", item.properties.keys())
        item.validate()

    def test_create_collection(self):
        collection = create_collection(AGGREGATED)
        collection.set_root(None)
        collection.validate()

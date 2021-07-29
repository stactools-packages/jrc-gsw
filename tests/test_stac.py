import re
import unittest

from stactools.jrc_gsw.constants import ID_REGEX
from stactools.jrc_gsw.stac import create_collection, create_item

from tests import test_data


class TestSTAC(unittest.TestCase):
    def test_create_item(self):
        args = {
            "change_href": test_data.get_path("data-files/change_0E_40Nv1_3_2020.tif"),
            "extent_href": test_data.get_path("data-files/extent_0E_40Nv1_3_2020.tif"),
            "occurrence_href": test_data.get_path(
                "data-files/occurrence_0E_40Nv1_3_2020.tif"
            ),
            "recurrence_href": test_data.get_path(
                "data-files/recurrence_0E_40Nv1_3_2020.tif"
            ),
            "seasonality_href": test_data.get_path(
                "data-files/seasonality_0E_40Nv1_3_2020.tif"
            ),
            "transitions_href": test_data.get_path(
                "data-files/transitions_0E_40Nv1_3_2020.tif"
            ),
        }

        item = create_item(**args)

        self.assertEqual(item.id, "0E_40Nv1_3_2020")

        for key, asset in item.assets.items():
            self.assertIn(key, asset.href)

        item.validate()

    def test_create_collection(self):
        collection = create_collection()
        collection.set_root(None)
        collection.validate()

    def test_item_id_parsing(self):
        paths = ["change/change_110W_20Sv1_3_2020cog.tif"]

        for path in paths:
            self.assertIsNotNone(re.match(ID_REGEX, path))

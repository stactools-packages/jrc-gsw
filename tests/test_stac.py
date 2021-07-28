import unittest

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
        import json

        with open("item.json", "w") as f:
            json.dump(item.to_dict(), f, indent=2)
        item.validate()

    def test_create_collection(self):
        collection = create_collection()
        collection.set_root(None)
        import json

        with open("collection.json", "w") as f:
            json.dump(collection.to_dict(), f, indent=2)
        collection.validate()
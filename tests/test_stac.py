import unittest

from stactools.jrc_gsw.stac import create_collection, create_item

from tests import test_data


class TestSTAC(unittest.TestCase):
    def test_create_item(self):
        args = {
            "source": test_data.get_path("data-files"),
            "tile_id": "0000360000-0000480000",
        }

        item = create_item(**args)

        self.assertEqual(item.id, args["tile_id"])

        for key, asset in item.assets.items():
            self.assertIn(key, asset.href)

        item.validate()

    def test_create_collection(self):
        collection = create_collection()
        collection.set_root(None)
        collection.validate()

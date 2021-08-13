import unittest

from stactools.jrc_gsw.stac import create_collection, create_item

from tests import test_data


class TestSTAC(unittest.TestCase):
    def test_create_item(self):
        args = {
            "source": test_data.get_path("data-files"),
            "tile_id": "0000360000-0000480000",
            "year": 1984,
            "month": 4,
        }

        item = create_item(**args)

        self.assertEqual(
            item.id, f'{args["tile_id"]}_{args["year"]}_{str(args["month"]).zfill(2)}'
        )

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
            self.assertIn(args["tile_id"], asset.href)

        item.validate()

    def test_create_collection(self):
        collection = create_collection()
        collection.set_root(None)
        collection.validate()

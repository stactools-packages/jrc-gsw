import os.path
from tempfile import TemporaryDirectory

import pystac

from stactools.jrc_gsw.commands import create_jrc_gsw_command

from stactools.testing import CliTestCase

from tests import test_data


class CreateCollectionTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_jrc_gsw_command]

    def test_create_collection(self):
        with TemporaryDirectory() as tmp_dir:
            result = self.run_command(["jrc-gsw", "create-collection", "-d", tmp_dir])
            self.assertEqual(result.exit_code, 0, msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            collection = pystac.read_file(os.path.join(tmp_dir, jsons[0]))
            child_links = collection.get_child_links()
            self.assertEqual(len(child_links), 4)

            collection.validate()

    def test_create_item(self):
        with TemporaryDirectory() as tmp_dir:
            test_cog = os.path.join(
                test_data.get_path("data-files"),
                "Aggregated",
                "LATEST",
                "change",
                "tiles",
                "change-0000360000-0000480000.tif",
            )
            result = self.run_command(
                ["jrc-gsw", "create-item", "-d", tmp_dir, "-s", test_cog]
            )
            self.assertEqual(result.exit_code, 0, msg="\n{}".format(result.output))

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)

            item_path = os.path.join(tmp_dir, jsons[0])

            item = pystac.read_file(item_path)

        item.validate()

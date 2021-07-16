import unittest

import stactools.jrc_gsw


class TestModule(unittest.TestCase):
    def test_version(self):
        self.assertIsNotNone(stactools.jrc_gsw.__version__)

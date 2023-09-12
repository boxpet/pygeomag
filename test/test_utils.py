from unittest import TestCase

from pygeomag import __version__


class TestUtil(TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.1.0")

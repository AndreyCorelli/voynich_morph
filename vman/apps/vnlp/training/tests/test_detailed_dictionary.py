from unittest import TestCase

from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary


class TestDetailedDictionary(TestCase):
    def test_feed(self):
        path_src = '/home/andrey/sources/vman/vman/vman/corpus/raw/en'
        dd = DetailedDictionary.read_from_corpus(path_src)
        self.assertGreater(len(dd.words), 100)

import os
from unittest import TestCase

from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestDetailedDictionary(TestCase):
    def test_feed(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        dd = DetailedDictionary.read_from_folder(path_src)
        self.assertGreater(len(dd.words), 100)

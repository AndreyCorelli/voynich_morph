from unittest import TestCase

from apps.vnlp.corpus_manager import CorpusManager
from corpus.corpus_data import CORPUS_ROOT


class TestCorpusManager(TestCase):
    # run this "test" to rebuild cached "corpus" files like
    # vman/corpus/features/en/alan_flower_001.json ...
    def test_rebuild_corpus_by_text(self):
        CorpusManager.read_corpus_by_text(CORPUS_ROOT, ignore_cached=True)

    # run this "test" to rebuild cached "corpus" folders - files
    # like vman/corpus/features/en.json
    def test_rebuild_corpus_by_language(self):
        CorpusManager.read_corpus_by_lang(CORPUS_ROOT, ignore_cached=True)

import os
from unittest import TestCase

from vman.apps.vnlp.training.alphabet import EnAlphabet, SlavAlphabet, RuAlphabet
from vman.apps.vnlp.training.raw_corpus_downloader import RawCorpusDownloader
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestRawCorpusDownloader(TestCase):
    def test_feed_en(self):
        path_src = '/home/andrey/Downloads/src_files/text/en_classic'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'en')
        RawCorpusDownloader.download(path_src, path_dst, EnAlphabet)

    def test_feed_slav(self):
        path_src = '/home/andrey/Downloads/src_files/text/slav_classic'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'slav')
        RawCorpusDownloader.download(path_src, path_dst, SlavAlphabet)

    def test_feed_ru(self):
        path_src = '/home/andrey/Downloads/src_files/text/ru_classic'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'ru')
        RawCorpusDownloader.download(path_src, path_dst, RuAlphabet)

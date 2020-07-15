import os
from unittest import TestCase

from apps.vnlp.training.alphabet import EnAlphabet, SlavAlphabet, RuAlphabet, \
    LatinAlphabet, EvaBasicAlphabetA, GreekAlphabet, PolishAlphabet
from apps.vnlp.training.eva_processor import EvaProcessor
from apps.vnlp.training.raw_corpus_downloader import RawCorpusDownloader
from corpus.corpus_data import RAW_CORPUS_ROOT


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

    def test_feed_polish(self):
        path_src = '/home/andrey/Downloads/src_files/text/polsky'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'polsky')
        RawCorpusDownloader.download(path_src, path_dst, PolishAlphabet)

    def test_feed_lat(self):
        path_src = '/home/andrey/Downloads/src_files/text/latin'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'lat')
        RawCorpusDownloader.download(path_src, path_dst, LatinAlphabet)

    def test_feed_greek(self):
        path_src = '/home/andrey/Downloads/src_files/text/greek'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'greek')
        RawCorpusDownloader.download(path_src, path_dst, GreekAlphabet)

    def test_feed_eva_basic_a(self):
        path_src = '/home/andrey/Downloads/src_files/text/vman'
        path_dst = os.path.join(RAW_CORPUS_ROOT, 'eba')
        RawCorpusDownloader.download(path_src, path_dst, EvaBasicAlphabetA,
                                     encoding='utf-8', processor=EvaProcessor)

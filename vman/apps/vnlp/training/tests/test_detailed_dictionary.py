import os
from unittest import TestCase

from apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from corpus.corpus_data import RAW_CORPUS_ROOT


class TestDetailedDictionary(TestCase):
    def test_feed(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        dd = DetailedDictionary.read_from_folder(path_src)
        self.assertGreater(len(dd.words), 100)

    def test_serialize_deserialize(self):
        dd = DetailedDictionary()
        dd.files_processed = 1
        dd.words_processed = 4
        dd.words.append(WordCard('detail', 12, 'tail'))
        dd.words[0].prefix = 'de'
        dd.words.append(WordCard('corpus', 2, ''))
        dd.words.append(WordCard('plural', 1, ''))
        dd.words.append(WordCard('omnis', 1, ''))
        dd.words_total = len(dd.words)
        dd.word_grams = {(2, 'corpus omins'): 24,
                         (3, 'plural corpus omins'): 21}
        jsn = dd.json_serialize()
        self.assertGreater(len(jsn), 10)

        rd = DetailedDictionary.json_deserialize(jsn)
        self.assertEqual(dd.files_processed, rd.files_processed)
        self.assertEqual(dd.words_processed, rd.words_processed)
        self.assertEqual(dd.words_total, rd.words_total)
        self.assertEqual(len(dd.words), len(rd.words))
        self.assertEqual(len(dd.word_grams), len(rd.word_grams))

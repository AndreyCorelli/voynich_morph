from unittest import TestCase

from vman.apps.vnlp.training.featurizers.word_morph_featurizer import WordMorphFeaturizer
from vman.corpus.corpus_data import CORPUS_ROOT


class TestWordMorphFeaturizer(TestCase):
    def test_features(self):
        path_src = CORPUS_ROOT
        ftz = WordMorphFeaturizer()
        features_by_lang = ftz.featurize_folder(path_src)
        langs = [l for l in features_by_lang]
        self.assertGreater(len(langs), 1)
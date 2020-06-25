from unittest import TestCase

from vman.apps.vnlp.training.classifiers.random_forest_classifier import RandomForestLangClassifier
from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.featurizers.word_morph_featurizer import WordMorphFeaturizer
from vman.corpus.corpus_data import CORPUS_ROOT


class TestRandomForestClassifier(TestCase):
    def test_split(self):
        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusFeatures.load_from_folder(CORPUS_ROOT)
        train, test = clsf.split_train_test(all_records)
        self.assertEqual(len(all_records), len(train) + len(test))

    def test_train_predict(self):
        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusFeatures.load_from_folder(CORPUS_ROOT)
        train, test = clsf.split_train_test(all_records)
        lang_id = RandomForestLangClassifier.encode_languages(all_records)
        id_lang = {lang_id[l]: l for l in lang_id}

        clsf.train_on_files(train, all_records)
        test_classes = clsf.classify(test)
        for i in range(len(test)):
            lang = id_lang.get(test_classes[i]) or '-'
            print(f'{test[i]}, lang classified as "{lang}"')

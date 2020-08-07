import random
from unittest import TestCase

from apps.vnlp.corpus_manager import CorpusManager
from apps.vnlp.training.classifiers.random_forest_classifier import RandomForestLangClassifier
from apps.vnlp.training.featurizers.word_morph_featurizer import WordMorphFeaturizer
from corpus.corpus_data import CORPUS_ROOT

# comment this line out for the result not to be deterministic
random.seed(1)


class TestRandomForestClassifier(TestCase):
    def test_split(self):
        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusManager.read_corpus_by_text(CORPUS_ROOT)
        train, test = clsf.split_train_test(all_records)
        self.assertEqual(len(all_records), len(train) + len(test))

    def test_train_predict(self):
        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusManager.read_corpus_by_text(CORPUS_ROOT)
        all_records = [r for r in all_records if r.language != 'eba']
        train, test = clsf.split_train_test(all_records)
        lang_id = RandomForestLangClassifier.encode_languages(all_records)
        id_lang = {lang_id[l]: l for l in lang_id}

        clsf.train_on_files(train, all_records)
        test_classes = clsf.classify(test)
        misses = sum([1 for i in range(len(test)) if test[i].language != id_lang.get(test_classes[i])])
        print(f'{misses} misses out of {len(test)} tests')
        for i in range(len(test)):
            lang = id_lang.get(test_classes[i]) or '-'
            prefix = '* ' if test[i].language != lang else ''
            print(f'{prefix}{test[i]}, lang classified as "{lang}"')

    def test_predict_voynich(self):
        v_langs = {'eba'}

        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusManager.read_corpus_by_text(CORPUS_ROOT)
        train = [r for r in all_records if r.language not in v_langs]
        test = [r for r in all_records if r.language in v_langs]

        lang_id = RandomForestLangClassifier.encode_languages(train)
        id_lang = {lang_id[l]: l for l in lang_id}

        clsf.train_on_files(train, train)
        test_classes = clsf.classify_vector(test)[0]
        m_index, mval = 0, 0
        for i in range(len(test_classes)):
            if test_classes[i] > mval:
                mval = test_classes[i]
                m_index = i

        lang = id_lang.get(m_index) or '-'
        print(f'EBA-encoded, Lang classified as "{lang}", probability estimated as {mval}')

        clsf.visualize('/home/andrey/Downloads/src_files/text/', WordMorphFeaturizer)

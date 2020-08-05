# comment this line out for the result not to be deterministic
import codecs
import os
import random
import tempfile
from shutil import rmtree
from unittest import TestCase

from transliterate import translit

from apps.vnlp.corpus_manager import CorpusManager
from apps.vnlp.training.classifiers.random_forest_classifier import RandomForestLangClassifier
from apps.vnlp.training.featurizers.word_morph_featurizer import WordMorphFeaturizer
from corpus.corpus_data import CORPUS_ROOT

random.seed(1)


class TestTransliteratedText(TestCase):
    def test_predict_transliterated(self):

        clsf = RandomForestLangClassifier(WordMorphFeaturizer())
        all_records = CorpusManager.read_corpus_by_text(CORPUS_ROOT)
        train = [r for r in all_records if not r.corpus_path.endswith('rachel_gray_001.txt')]

        # get full path to the source text file
        test_corpus = [r for r in all_records if r.corpus_path.endswith('rachel_gray_001.txt')]
        with codecs.open(test_corpus[0].corpus_path, 'r', encoding='utf-8') as fr:
            source_file_text = fr.read()

        # transliterate
        trans_text = translit(source_file_text, 'el')

        tmp_dir = tempfile.mkdtemp()
        try:
            subfolder = os.path.join(tmp_dir, 'raw')
            os.mkdir(subfolder)
            subfolder = os.path.join(subfolder, 'greek')
            os.mkdir(subfolder)
            tmp_filename = os.path.join(subfolder, 'tmp.txt')

            with codecs.open(tmp_filename, 'w', encoding='utf-8') as fw:
                fw.write(trans_text)
            test_corpus = CorpusManager.read_corpus_by_text(
                folder=tmp_dir,
                ignore_cached=True, file_name_only='tmp.txt')
            
            lang_id = RandomForestLangClassifier.encode_languages(train)
            id_lang = {lang_id[l]: l for l in lang_id}

            clsf.train_on_files(train, all_records)
            test_classes = clsf.classify_vector(test_corpus)[0]

        finally:
            rmtree(tmp_dir)
        m_index, mval = 0, 0
        for i in range(len(test_classes)):
            if test_classes[i] > mval:
                mval = test_classes[i]
                m_index = i

        lang = id_lang.get(m_index) or '-'
        print(f'[en] rachel_gray_001, Lang classified as "{lang}", probability estimated as {mval}')

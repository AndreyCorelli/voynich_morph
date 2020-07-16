import os
from typing import List, Optional

from apps.vnlp.training.alphabet import alphabet_by_code
from apps.vnlp.training.corpus_features import CorpusFeatures
from apps.vnlp.training.detailed_dictionary import DetailedDictionary
from corpus.corpus_data import CORPUS_ROOT


class CorpusManager:
    @classmethod
    def read_corpus_by_text(cls,
                            folder: str = CORPUS_ROOT,
                            ignore_cached: bool = False,
                            read_cached_only: bool = False) -> List[CorpusFeatures]:
        """
        "folder" should have the following structure:
         - raw
           - <lang_1>
             - <file_1_1>.txt  # source text - words in lowercase, space-separated
             ..
           - <lang_N>
         - features
           - <file_1_1>.json  # JSON-encoded CorpusFeatures for file_1_1.txt "corpus"
           ..

        """
        data = []  # type: List[CorpusFeatures]

        raw_path = os.path.join(folder, 'raw')
        features_path = os.path.join(folder, 'features')
        if not os.path.isdir(features_path):
            os.mkdir(features_path)

        dirs = [f for f in os.listdir(raw_path)]
        for dir_name in dirs:
            sub_path = os.path.join(raw_path, dir_name)
            if not os.path.isdir(sub_path):
                continue

            language = dir_name  # now we somwhere like '.../raw/fr/'
            files = [f for f in os.listdir(sub_path)]
            for file_name in files:
                full_path = os.path.join(sub_path, file_name)  # '.../raw/fr/file01.txt'
                if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                    continue
                # try "cached" feature file
                features_name = os.path.splitext(file_name)[0] + '.json'
                feature_path = os.path.join(features_path, dir_name, features_name)
                corpus = None  # type: Optional[CorpusFeatures]
                if not ignore_cached and os.path.isfile(feature_path):
                    try:
                        cf = CorpusFeatures.load_from_file(feature_path)
                        if cf.version != CorpusFeatures.ACTUAL_VERSION:
                            print(f'File "{feature_path}" has version "{cf.version}"')
                        else:
                            corpus = cf
                    except Exception as e:
                        print(f'Error loading "{feature_path}": {e}')
                if not corpus and not read_cached_only:
                    # build corpus
                    alph = alphabet_by_code[language]
                    corpus = CorpusFeatures(language, alph, full_path)
                    dict = DetailedDictionary.read_from_file(full_path)
                    corpus.build(dict)
                    # cache corpus
                    feature_subfolder = os.path.join(features_path, dir_name)
                    if not os.path.isdir(feature_subfolder):
                        os.mkdir(feature_subfolder)
                    corpus.save_to_file(feature_path)

                if corpus:
                    data.append(corpus)
        return data

    @classmethod
    def read_corpus_by_lang(cls,
                            folder: str = CORPUS_ROOT,
                            ignore_cached: bool = False,
                            read_cached_only: bool = False) -> List[CorpusFeatures]:
        """
        Almost the same as read_corpus_by_text, but combines all texts by language
        into single corpus
        """
        data = []  # type: List[CorpusFeatures]

        raw_path = os.path.join(folder, 'raw')
        features_path = os.path.join(folder, 'features')
        if not os.path.isdir(features_path):
            os.mkdir(features_path)

        dirs = [f for f in os.listdir(raw_path)]
        for dir_name in dirs:
            sub_path = os.path.join(raw_path, dir_name)
            if not os.path.isdir(sub_path):
                continue

            language = dir_name
            features_name = f'{language}.json'  # '.../raw/fr.json'
            feature_path = os.path.join(features_path, features_name)
            corpus = None

            if not ignore_cached and os.path.isfile(feature_path):
                try:
                    cf = CorpusFeatures.load_from_file(feature_path)
                    if cf.version != CorpusFeatures.ACTUAL_VERSION:
                        print(f'File "{feature_path}" has version "{cf.version}"')
                    else:
                        corpus = cf
                except Exception as e:
                    print(f'Error loading "{feature_path}": {e}')

            if not corpus and not read_cached_only:
                # build corpus
                alph = alphabet_by_code[language]
                corpus = CorpusFeatures(language, alph, sub_path)
                dict = DetailedDictionary.read_from_folder(sub_path)
                corpus.build(dict)
                # cache corpus
                corpus.save_to_file(feature_path)
            if corpus:
                data.append(corpus)
        return data

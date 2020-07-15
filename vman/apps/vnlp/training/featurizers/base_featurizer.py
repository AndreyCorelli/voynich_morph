import codecs
from typing import List, Dict, Tuple

from apps.vnlp.training.corpus_features import CorpusFeatures


class BaseFeaturizer:
    def featurize_folder(self, corpus_folder: str) -> Dict[str, List[Tuple[str, List[float]]]]:
        """
        Folder structure should correspond to the one used by
        CorpusFeatures.load_from_folder() method, i.e.:
         raw/en/file1.txt ...
         features/en/file1.txt ...
        """
        features_by_lang = {}  # type: Dict[str, List[Tuple[str, List[float]]]]
        corpus_by_lang = CorpusFeatures.load_from_folder(corpus_folder)
        for lang in corpus_by_lang:
            corpuses = corpus_by_lang[lang]
            if not corpuses:
                continue
            feature_list = []
            features_by_lang[lang] = feature_list

            for corpus in corpuses:
                feature_list.append(self.featurize_corpus(corpus))

        return features_by_lang

    def featurize_corpus(self, corpus: CorpusFeatures) -> List[float]:
        src_path = corpus.corpus_path
        with codecs.open(src_path, 'r', encoding='utf-8') as fr:
            text = fr.read()
        words = text.split(' ')
        return self.featurize_words(words, corpus)

    def featurize_words(self, words: List[str], corpus: CorpusFeatures) -> List[float]:
        raise NotImplementedError()

    @classmethod
    def get_feature_names(self) -> List[str]:
        raise NotImplementedError()

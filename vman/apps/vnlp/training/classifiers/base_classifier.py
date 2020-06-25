import random
from typing import List, Tuple, Dict

from vman.apps.vnlp.training.corpus_features import CorpusCollectionRecord
from vman.apps.vnlp.training.featurizers.base_featurizer import BaseFeaturizer


class BaseClassifier:
    def __init__(self,
                 featurizer: BaseFeaturizer):
        self.featurizer = featurizer
        self.lang_code = {}  # type: Dict[str, int]

    @classmethod
    def split_train_test(
            cls,
            src: List[CorpusCollectionRecord],
            test_percent=20) -> Tuple[List[CorpusCollectionRecord],
                                      List[CorpusCollectionRecord]]:
        dst = list(src)
        random.shuffle(dst)
        index = round((100 - test_percent) * len(dst) / 100)
        return dst[:index], dst[index:]

    @classmethod
    def encode_languages(cls, all_records: List[CorpusCollectionRecord]) -> Dict[str, int]:
        langs = {r.language for r in all_records}
        langs_list = [l for l in langs]
        langs_list.sort()
        lang_id = {}  # type: Dict[str, int]
        for i in range(len(langs_list)):
            lang_id[langs_list[i]] = i + 1
        return lang_id

    def train_on_files(self,
                       train_records: List[CorpusCollectionRecord],
                       all_records: List[CorpusCollectionRecord]):
        if not self.lang_code:
            self.lang_code = self.encode_languages(all_records)
        x, y = self.get_x_y(train_records)
        self._train(x, y)

    def classify(self, unclassified_records: List[CorpusCollectionRecord]) -> List[float]:
        x, _ = self.get_x_y(unclassified_records)
        return self._classify(x)

    def _train(self, x: List[List[float]], y: List[float]):
        raise NotImplementedError()

    def _classify(self, x: List[List[float]]) -> List[float]:
        raise NotImplementedError()

    def get_x_y(self, train_records: List[CorpusCollectionRecord]) -> Tuple[List[List[float]], List[float]]:
        x = []  # type: List[List[float]]
        y = []  # type: List[float]
        for corpus in train_records:
            x.append(self.featurizer.featurize_corpus(corpus.features))
            y.append(self.lang_code.get(corpus.language) or 0)
        return x, y

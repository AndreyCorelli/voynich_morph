from typing import List

from apps.vnlp.training.corpus_features import CorpusFeatures
from corpus.corpus_data import CORPUS_ROOT


class CorpusManager:
    @classmethod
    def read_corpus_by_text(cls,
                            ignore_cached: bool,
                            read_cached_only: bool) -> List[CorpusFeatures]:
        return CorpusFeatures.load_from_folder(CORPUS_ROOT, ignore_cached, read_cached_only)
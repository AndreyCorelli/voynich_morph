from typing import List, Tuple, Dict

from apps.vnlp.training.corpus_features import CorpusFeatures
from apps.vnlp.training.detailed_dictionary import WordCard


class CorpusBrief:
    def __init__(self):
        self.words_by_morph = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_by_root = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_total = 0

    def to_dict(self):
        return {
            'words_by_morph': self.words_by_morph,
            'words_by_root': self.words_by_root,
            'words_total': self.words_total
        }

    def build_from_corpus(self, f: CorpusFeatures):
        # build most popula
        max_len = 7
        top_count = 30

        self.words_total = sum([w.count for w in f.dictionary.words])

        dict_src = [(self.words_by_morph, 'morph',),
                    (self.words_by_root, 'root',)]

        for dct, sort_key in dict_src:
            words = list(f.dictionary.words)
            if sort_key == 'morph':
                words.sort(key=lambda w: -w.count)
            else:
                words.sort(key=lambda w: -w.root_count)

            for char_count in range(1, max_len):
                wrd_list = []
                dct[char_count] = wrd_list
                for w in words:  # type: WordCard
                    if len(w.word) < char_count:
                        continue
                    wrd_list.append((w.word, w.root, w.prefix, w.suffix, w.count,))
                    if len(wrd_list) == top_count:
                        break


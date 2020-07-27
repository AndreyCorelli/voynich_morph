from typing import List, Tuple, Dict

from apps.vnlp.training.corpus_features import CorpusFeatures
from apps.vnlp.training.detailed_dictionary import WordCard


class CorpusBrief:
    def __init__(self):
        self.words_by_morph = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_by_root = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_total = 0
        self.word_grams = {}  # type: Dict[int, List[str, int]]

    def to_dict(self):
        return {
            'words_by_morph': self.words_by_morph,
            'words_by_root': self.words_by_root,
            'words_total': self.words_total,
            'word_grams': self.word_grams
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

        for wg_len, wg in f.dictionary.word_grams:
            ngr_dict = self.word_grams.get(wg_len)
            if not ngr_dict:
                ngr_dict = []
                self.word_grams[wg_len] = ngr_dict
            ngr_dict.append((wg, f.dictionary.word_grams[(wg_len, wg,)],))

        for wg_len in self.word_grams:
            self.word_grams[wg_len].sort(key=lambda w: -w[1])
            self.word_grams[wg_len] = self.word_grams[wg_len][:30]

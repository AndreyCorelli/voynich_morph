import codecs
import os
from typing import List, Tuple, Dict

from apps.vnlp.training.corpus_features import CorpusFeatures
from apps.vnlp.training.detailed_dictionary import WordCard


class CorpusBrief:
    def __init__(self):
        self.words_by_morph = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_by_root = {}  # type: Dict[int, List[Tuple[str, str, str, str, int]]]
        self.words_total = 0
        self.word_grams = {}  # type: Dict[int, List[str, int]]
        self.symbol_frequency = []  # type: List[str, float]

    def to_dict(self):
        return {
            'words_by_morph': self.words_by_morph,
            'words_by_root': self.words_by_root,
            'words_total': self.words_total,
            'word_grams': self.word_grams,
            'symbol_frequency': self.symbol_frequency
        }

    def build_from_corpus(self, f: CorpusFeatures):
        # build most popular
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

        self.calculate_symbol_frequency(f)

    def calculate_symbol_frequency(self, f: CorpusFeatures):
        smb_count = {}  # type: Dict[str, int]
        if os.path.isfile(f.corpus_path):
            self.calculate_symbol_frequency_in_file(f.corpus_path, smb_count)
        else:
            files = [f for f in os.listdir(f.corpus_path)]
            for file_name in files:
                full_path = os.path.join(f.corpus_path, file_name)
                if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                    continue
                self.calculate_symbol_frequency_in_file(full_path, smb_count)
        total = sum([smb_count[s] for s in smb_count])
        self.symbol_frequency = [(s, smb_count[s] / total,) for s in smb_count]
        self.symbol_frequency.sort(key=lambda s: -s[1])

    def calculate_symbol_frequency_in_file(self, file_path: str, smb_count: Dict[str, int]):
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                if c == ' ' or c == '\n':
                    continue
                ct = smb_count.get(c) or 0
                smb_count[c] = ct + 1

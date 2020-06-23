import json
from typing import Dict, List, Tuple, Optional

from vman.apps.vnlp.training.alphabet import Alphabet
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard


class MarginNgram:
    """
    Prefix or suffix
    """
    def __init__(self,
                 text: str,
                 direct: int,
                 dic_occurs: int = 0,
                 modified_count: int = 0):
        self.text = text
        self.direct = direct  # 1 for prefix, -1 for suffix
        self.dic_occurs = dic_occurs  # number of occurrences among all dict records
        self.modified_count = modified_count  # number of words that appear both with and w/o this ngram

    def __repr__(self):
        ps = 'prefix' if self.direct == 1 else 'suffix'
        return f'{self.text} ({ps}, {self.dic_occurs})'

    def is_in_word(self, word: str, alphabet: Alphabet) -> bool:
        if self.direct == 1:  # prefix
            if not word.startswith(self.text):
                return False
        else:
            if not word.endswith(self.text):
                return False
        rem_len = len(word) - len(self.text)
        return rem_len >= alphabet.root_min

    def chop_from_word(self, word: str, alphabet: Alphabet) -> Optional[str]:
        if not self.is_in_word(word, alphabet):
            return None
        return word[len(self.text):] if self.direct == 1 \
            else word[:-len(self.text)]

    def add_to_word(self, word: str) -> Optional[str]:
        return self.text + word if self.direct == 1 else word + self.text


class MarginNgramsCollector:
    def __init__(self,
                 alphabet: Alphabet,
                 dictionary: DetailedDictionary):
        self.alphabet = alphabet
        self.dictionary = dictionary
        if self.dictionary:
            self.unique_words = {w.word for w in dictionary.words}
        else:
            self.unique_words = {}
        self.prefixes = []  # type: List[MarginNgram]
        self.suffixes = []  # type: List[MarginNgram]
        self.all_grams = []  # type: List[MarginNgram]

    def build(self):
        prefixes = {}
        suffixes = {}
        for word in self.dictionary.words:  # type: WordCard
            for i in range(self.alphabet.prefix_min, self.alphabet.prefix_max + 1):
                reminder = len(word.word) - i
                if reminder < self.alphabet.prefix_min:
                    break
                prefix = word.word[:i]
                pref_count = prefixes.get(prefix) or 0
                prefixes[prefix] = pref_count + 1  # word.count
            for i in range(self.alphabet.suffix_min, self.alphabet.suffix_max + 1):
                reminder = len(word.word) - i
                if reminder < self.alphabet.prefix_min:
                    break
                suffix = word.word[-i:]
                suffix_count = suffixes.get(suffix) or 0
                suffixes[suffix] = suffix_count + 1  # word.count

        # remove rare cases
        threshold = 0.005
        min_count = int(self.dictionary.words_total * threshold)
        for sfx in prefixes:
            if prefixes[sfx] >= min_count:
                self.prefixes.append(MarginNgram(sfx, 1, prefixes[sfx]))
        for sfx in suffixes:
            if suffixes[sfx] >= min_count:
                self.suffixes.append(MarginNgram(sfx, -1, suffixes[sfx]))

        # self.filter_by_orig_morph()
        # self.filter_by_ngram_inclusion()

        self.prefixes.sort(key=lambda p: -len(p.text) * 1000 - p.dic_occurs)
        self.suffixes.sort(key=lambda p: -len(p.text) * 1000 - p.dic_occurs)
        #self.prefixes = [p for p in self.prefixes if p.modified_count > 1]
        #self.suffixes = [p for p in self.suffixes if p.modified_count > 1]
        self.all_grams = self.suffixes + self.prefixes

    def filter_by_ngram_inclusion(self):
        # subtract dic_occurs / modified_count numbers
        # where the ngram is consumed by longer ngram, like
        # "ion" (tensION) "consumes" "on" (tensiON)
        src = [self.prefixes, self.suffixes]
        directions = [1, -1]
        for collection, direct in zip(src, directions):
            for ngram in collection:
                consumers = [c for c in collection if c.text.startswith(ngram.text) \
                             and len(c.text) > len(ngram.text)] if direct else \
                            [c for c in collection if c.text.endswith(ngram.text) \
                             and len(c.text) > len(ngram.text)]
                if consumers:
                    for word in self.dictionary.words:
                        if not ngram.is_in_word(word.word, self.alphabet):
                            continue
                        for cs in consumers:
                            if cs.is_in_word(word.word, self.alphabet):
                                ngram.modified_count -= 1
                                ngram.dic_occurs -= 1
                                break

    def filter_by_orig_morph(self):
        # be sure that there's a word w/o suffix / prefix
        # in the dictionary for each potential suffix / prefix
        src = [self.prefixes, self.suffixes]
        directions = [1, -1]
        for collection, direct in zip(src, directions):
            for item in collection:
                for word in self.dictionary.words:  # type: WordCard
                    if direct == 1:  # prefix
                        if not word.word.startswith(item.text):
                            continue
                        word_root = word.word[len(item.text):]
                        if len(word_root) < self.alphabet.root_min:
                            continue
                        if word_root in self.unique_words:
                            item.modified_count += 1
                    else:  # suffix
                        if not word.word.endswith(item.text):
                            continue
                        word_root = word.word[:len(item.text)]
                        if len(word_root) < self.alphabet.root_min:
                            continue
                        if word_root in self.unique_words:
                            item.modified_count += 1

    def json_serialize(self) -> str:
        data = [{
            'text': n.text,
            'direct': n.direct,
            'dic_occurs': n.dic_occurs,
            'modified_count': n.modified_count
        } for n in self.all_grams]
        return json.dumps(data)

    @classmethod
    def json_deserialize(cls, data_str: str):  # MarginNgramsCollector
        data = json.loads(data_str)
        collector = MarginNgramsCollector(None, None)
        for dic in data:
            mgr = MarginNgram(dic['text'], dic['direct'],
                              dic['dic_occurs'], dic['modified_count'])
            collector.all_grams.append(mgr)
            if mgr.direct == 1:
                collector.prefixes.append(mgr)
            else:
                collector.suffixes.append(mgr)
        return collector

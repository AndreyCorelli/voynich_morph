from typing import Optional, Set, Dict, List, Tuple

from vman.apps.vnlp.training.alphabet import Alphabet
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from vman.apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram


class CorpusFeatures:
    def __init__(self,
                 language: str,
                 alphabet: Alphabet,
                 corpus_path: str):
        self.language = language
        self.alphabet = alphabet
        self.corpus_path = corpus_path
        self.dictionary = None  # type: Optional[DetailedDictionary]
        self.ngrams_collector = None  # type: Optional[MarginNgramsCollector]
        self.all_words = set()  # type: Set[str]

    def build(self):
        self.dictionary = DetailedDictionary.read_from_corpus(self.corpus_path)
        self.all_words = {d.word for d in self.dictionary.words}
        self.ngrams_collector = MarginNgramsCollector(self.alphabet, self.dictionary)
        self.ngrams_collector.build()
        self.find_dict_morphs()

    def encode_words_by_morphs(self, words: List[str]) -> List[Tuple[float, float, float]]:
        coded = []  # type: List[Tuple[float, float, float]]
        total = float(sum([w.count for w in self.dictionary.words]))
        word_freq = {w.word: w.root_count / total for w in self.dictionary.words}
        word_cards = {w.word: w for w in self.dictionary.words}

        for word in words:
            freq = word_freq.get(word) or 0
            pf, sf = 0.0, 0.0
            card = word_cards.get(word)  # type: WordCard
            if card:
                if card.prefix:
                    pf = 1.0
                if card.suffix:
                    sf = 1.0
            coded.append((freq, pf, sf,))
        return coded

    def find_dict_morphs(self):
        for word in self.dictionary.words:  # type: WordCard
            possible_roots = self.get_possible_roots(word.word)
            root_word = self.check_possible_roots(possible_roots)
            if root_word:
                word.root = root_word.root
                word.prefix = root_word.prefix
                word.suffix = root_word.suffix
            else:
                word.root = word.word
        self.count_roots()

    def count_roots(self):
        words_by_root = {}  # type: Dict[str, List[WordCard]]
        for word in self.dictionary.words:
            if word.root not in words_by_root:
                words_by_root[word.root] = [word]
            else:
                words_by_root[word.root].append(word)
        for root in words_by_root:
            root_count = sum([wr.count for wr in words_by_root[root]])
            for word in words_by_root[root]:
                word.root_count = root_count

    def get_possible_roots(
            self,
            word: str) -> List[WordCard]:
        roots = {}  # Dict[str, WordCard]
        prefs = [None] + self.ngrams_collector.prefixes
        suffs = [None] + self.ngrams_collector.suffixes
        for pref in prefs:
            for suf in suffs:
                chopped = pref.chop_from_word(word, self.alphabet) if pref else word
                if not chopped:
                    continue
                chopped = suf.chop_from_word(chopped, self.alphabet) if suf else chopped
                if chopped:
                    card = WordCard(word)
                    card.root = chopped
                    card.prefix = pref.text if pref else ''
                    card.suffix = suf.text if suf else ''
                    roots[f'{card.prefix}+{chopped}+{card.suffix}'] = card
        del roots[f'+{word}+']
        root_list = [roots[r] for r in roots]
        root_list.sort(key=lambda r: len(r.word))
        return root_list

    def check_possible_roots(
            self,
            roots: List[WordCard]) -> Optional[WordCard]:
        prefixes = [None] + self.ngrams_collector.prefixes
        suffixes = [None] + self.ngrams_collector.suffixes

        for root in roots:
            for pref in prefixes:
                for suf in suffixes:
                    modf = pref.text + root.root if pref else root.root
                    modf = modf + suf.text if suf else modf
                    if modf in self.all_words:
                        return root
        return None

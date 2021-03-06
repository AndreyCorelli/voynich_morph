import codecs
import os
import json
from typing import Optional, Set, Dict, List, Tuple

from apps.vnlp.training.alphabet import Alphabet, alphabet_by_code
from apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram


class CorpusFeatures:
    ACTUAL_VERSION = '1.2'

    def __init__(self,
                 language: str,
                 alphabet: Alphabet,
                 corpus_path: str):
        self.version = self.ACTUAL_VERSION
        self.language = language
        self.alphabet = alphabet
        self.corpus_path = corpus_path
        self.dictionary = None  # type: Optional[DetailedDictionary]
        self.ngrams_collector = None  # type: Optional[MarginNgramsCollector]
        self.all_words = set()  # type: Set[str]
        self.multifile = False
        self.cache_file_path = ''

    def __repr__(self):
        corp_file = self.corpus_path or ''
        try:
            corp_file = os.path.basename(corp_file)
        except:
            pass
        return f'[{self.language}] - {corp_file}'

    @property
    def language_title(self):
        ab = alphabet_by_code.get(self.language)
        return ab.title if ab else '-'

    def build(self, dictionary: DetailedDictionary):
        self.dictionary = dictionary
        self.all_words = {d.word for d in self.dictionary.words}
        self.ngrams_collector = MarginNgramsCollector(self.alphabet, self.dictionary)
        self.ngrams_collector.build()
        self.find_dict_morphs()
        self.update_margin_ngrams()

    def save_to_file(self, path: str):
        data = {
            'version': self.version,
            'language': self.language,
            'alphabet': self.alphabet.__name__,
            'path': self.corpus_path,
            'dictionary': self.dictionary.json_serialize(),
            'ngrams_collector': self.ngrams_collector.json_serialize()
        }
        with codecs.open(path, 'w', encoding='utf-8') as fw:
            s = json.dumps(data)
            fw.write(s)

    @classmethod
    def load_from_file(cls, path: str):  # CorpusFeatures
        with codecs.open(path, 'rb') as fr:
            data = json.load(fr)
        alphabet = f'apps.vnlp.training.alphabet.{data["alphabet"]}'
        cf = CorpusFeatures(data['language'], alphabet, data['path'])
        cf.version = data['version']
        cf.dictionary = DetailedDictionary.json_deserialize(data['dictionary'])
        cf.ngrams_collector = MarginNgramsCollector.json_deserialize(data['ngrams_collector'])
        return cf

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

    def update_margin_ngrams(self):
        mgrams = {}  # type: Dict[Tuple[str, int], MarginNgram]
        for word in self.dictionary.words:
            word_grams = [(word.prefix, 1,), (word.suffix, -1,)]
            for word_gram, gram_dir in word_grams:
                if not word_gram:
                    continue
                mgram = mgrams.get((word_gram, gram_dir,))
                if mgram:
                    mgram.modified_count += 1
                    mgram.dic_occurs += word.count
                else:
                    mgrams[(word_gram, gram_dir,)] = \
                        MarginNgram(word_gram, gram_dir, word.count, 1)

        self.ngrams_collector.prefixes = []
        self.ngrams_collector.suffixes = []
        self.ngrams_collector.all_grams = []
        for key in mgrams:
            mgram = mgrams[key]
            self.ngrams_collector.all_grams.append(mgram)
            if mgram.direct == 1:
                self.ngrams_collector.prefixes.append(mgram)
            else:
                self.ngrams_collector.suffixes.append(mgram)

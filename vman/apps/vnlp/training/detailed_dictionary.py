import os
import codecs
from typing import List, Dict


class WordCard:
    def __init__(self, word: str, count: int = 1, root: str = ''):
        self.word = word
        self.root = root
        self.prefix = ''
        self.suffix = ''
        # count of the exact word (morph) in the dictionary
        self.count = count
        # count of the words with the same root (root_count >= count)
        self.root_count = 1

    def __repr__(self):
        pr = self.prefix + ']' if self.prefix else ''
        root = self.root if self.root else self.word
        sf = '[' + self.suffix if self.suffix else ''
        text = pr + root + sf
        return f'{text} (x{self.count})'


class DetailedDictionary:
    def __init__(self):
        self.words = []  # type:List[WordCard]
        self.words_total = 0

    @classmethod
    def read_from_corpus(cls, corpus_path: str):  # DetailedDictionary
        dd = DetailedDictionary()
        files = [f for f in os.listdir(corpus_path)]
        word_count = {}  # type: Dict[str, int]
        for file_name in files:
            full_path = os.path.join(corpus_path, file_name)
            if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                continue
            cls.read_file(full_path, word_count)

        for w in word_count:
            dd.words_total += 1
            dd.words.append(WordCard(w, word_count[w]))
        dd.words.sort(key=lambda w: w.word)
        #dd.words.sort(key=lambda w: -w.count)
        return dd

    @classmethod
    def read_file(cls, file_path: str, word_count: Dict[str, int]):
        with codecs.open(file_path, 'r', encoding='utf-8') as fr:
            text = fr.read()
        words = text.split(' ')
        for w in words:
            if not w:
                continue
            count = word_count.get(w) or 0
            word_count[w] = count + 1
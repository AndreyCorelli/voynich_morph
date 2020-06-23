import json
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
    def read_from_file(cls, file_path: str):  # DetailedDictionary
        dd = DetailedDictionary()
        word_count = {}  # type: Dict[str, int]
        cls.read_file(file_path, word_count)
        dd.build_word_cards(word_count)
        return dd

    @classmethod
    def read_from_folder(cls, corpus_folder: str):  # DetailedDictionary
        dd = DetailedDictionary()
        files = [f for f in os.listdir(corpus_folder)]
        word_count = {}  # type: Dict[str, int]
        for file_name in files:
            full_path = os.path.join(corpus_folder, file_name)
            if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                continue
            cls.read_file(full_path, word_count)
        dd.build_word_cards(word_count)
        return dd

    def build_word_cards(self, word_count: Dict[str, int]):
        for w in word_count:
            self.words_total += 1
            self.words.append(WordCard(w, word_count[w]))
        self.words.sort(key=lambda w: w.word)

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

    def json_serialize(self) -> str:
        data = {w.word: {
            'root': w.root,
            'prefix': w.prefix or '',
            'suffix': w.suffix or '',
            'count': w.count,
            'root_count': w.root_count
        } for w in self.words}
        return json.dumps(data)

    @classmethod
    def json_deserialize(cls, data_str: str):  # DetailedDictionary
        dd = DetailedDictionary()
        data = json.loads(data_str)
        for wrd in data:
            word = WordCard(wrd, data[wrd]['count'], data[wrd]['root'])
            word.prefix = data[wrd]['prefix']
            word.suffix = data[wrd]['suffix']
            word.root_count = data[wrd]['root_count']
            dd.words.append(word)
        dd.words_total = len(dd.words)
        return dd

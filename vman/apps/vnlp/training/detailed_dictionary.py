import json
import os
import codecs
from typing import List, Dict, Tuple


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
    NGRAMS_TO_STORE = 100

    def __init__(self):
        self.words = []  # type:List[WordCard]
        self.words_total = 0
        self.words_processed = 0
        self.files_processed = 0
        # {(3, 'so be it'): 19} - words, words count, occurrences
        self.word_grams = {}  # type: Dict[Tuple[int, str], int]

    @classmethod
    def read_from_file(cls, file_path: str):  # DetailedDictionary
        dd = DetailedDictionary()
        word_count = {}  # type: Dict[str, int]
        dd.read_file(file_path, word_count)
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
            dd.read_file(full_path, word_count)
        dd.build_word_cards(word_count)
        return dd

    def build_word_cards(self, word_count: Dict[str, int]):
        for w in word_count:
            self.words_total += 1
            self.words.append(WordCard(w, word_count[w]))
        self.words.sort(key=lambda w: w.word)

    def read_file(self, file_path: str, word_count: Dict[str, int]):
        with codecs.open(file_path, 'r', encoding='utf-8') as fr:
            text = fr.read()
        words = text.split(' ')

        cur_ngrams = [[2, []], [3, []]]
        for w in words:
            if not w:
                continue
            for ngram_len, ngram in cur_ngrams:
                ngram.append(w)
                if len(ngram) < ngram_len:
                    continue
                elif len(ngram) > ngram_len:
                    ngram.pop(0)
                ngrstr = ' '.join(ngram)
                ngr_key = (ngram_len, ngrstr,)
                ngr_item = self.word_grams.get(ngr_key)
                if not ngr_item:
                    self.word_grams[ngr_key] = 1
                else:
                    self.word_grams[ngr_key] = ngr_item + 1
            self.words_processed += 1
            count = word_count.get(w) or 0
            word_count[w] = count + 1
        self.files_processed += 1

    def json_serialize(self) -> str:
        ordered_ngrams = [(w[0], w[1], self.word_grams[w],) for w in self.word_grams]
        ordered_ngrams.sort(key=lambda w: -w[2])
        ngrams_selected = {k[1]: k[2] for k in ordered_ngrams[:self.NGRAMS_TO_STORE]}
        data = {
            'files_processed': self.files_processed,
            'words_processed': self.words_processed,
            'word_grams': ngrams_selected
        }
        data['words'] = {w.word: {
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

        dd.files_processed = data['files_processed']
        dd.words_processed = data['words_processed']
        word_grams = data['word_grams']
        for wg in word_grams:
            wg_len = sum([1 for c in wg if c == ' ']) + 1
            wg_key = (wg_len, wg,)
            dd.word_grams[wg_key] = word_grams[wg]

        words_data = data['words']
        for wrd in words_data:
            word = WordCard(wrd, words_data[wrd]['count'], words_data[wrd]['root'])
            word.prefix = words_data[wrd]['prefix']
            word.suffix = words_data[wrd]['suffix']
            word.root_count = words_data[wrd]['root_count']
            dd.words.append(word)
        dd.words_total = len(dd.words)
        return dd

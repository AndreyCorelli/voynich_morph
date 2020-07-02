import os
import codecs
from typing import Type

from vman.apps.vnlp.training.raw_text_processor import RawTextProcessor


class FileSplitStream:
    def __init__(self, file_path: str, min_words: int, max_words: int):
        self.file_path = file_path
        self.fw = None  # file writer
        self.word_counter = 0
        self.file_counter = 1
        self.min_words = min_words
        self.max_words = max_words
        self.last_path = ''

    def __enter__(self):
        return self

    def store_word(self, word: str):
        if self.word_counter >= self.max_words:
            self.fw.close()
            self.fw = None
            self.word_counter = 0
            self.file_counter += 1

        if not self.fw:
            self.last_path = f'{self.file_path}_{self.file_counter:03d}.txt'
            self.fw = codecs.open(self.last_path, 'w')

        self.fw.write(word + ' ')
        self.word_counter += 1

    def __exit__(self, type, value, traceback):
        if self.fw:
            self.fw.close()
        if self.word_counter < self.min_words and self.last_path:
            os.remove(self.last_path)


class RawCorpusDownloader:
    MIN_FILE_WORDS = 10 * 1000
    MAX_FILE_WORDS = 37 * 1000

    @classmethod
    def download(cls,
                 src_folder: str,
                 out_folder: str,
                 abet: Type,
                 encoding='utf-8',
                 processor: RawTextProcessor = None):
        processor = processor or RawTextProcessor
        files = [f for f in os.listdir(src_folder)]
        for file_name in files:
            full_path = os.path.join(src_folder, file_name)
            if not os.path.isfile(full_path):
                continue
            cls.download_file(full_path, out_folder, abet, encoding, processor)

    @classmethod
    def download_file(cls,
                      file_path: str,
                      out_folder: str,
                      abet: Type,
                      encoding: str,
                      processor: RawTextProcessor):
        name = os.path.splitext(os.path.basename(file_path))[0]
        with codecs.open(file_path, mode='r', encoding=encoding) as fr:
            file_text = fr.read()

        out_path = os.path.join(out_folder, name)
        with FileSplitStream(out_path, cls.MIN_FILE_WORDS, cls.MAX_FILE_WORDS) as fw:
            for word in processor.extract_words(file_text, abet):
                word = abet.preprocess_word(word)
                fw.store_word(word)

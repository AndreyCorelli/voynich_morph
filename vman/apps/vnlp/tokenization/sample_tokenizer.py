from typing import List, Tuple
import nltk
import codecs


class SampleTokenizer:
    def tokenize_file(self, src_path: str, output_path: str):
        with codecs.open(src_path, 'r', encoding='utf-8') as fr:
            txt = fr.read()
        tokenized = self.tokenize_text(txt)
        with codecs.open(src_path, 'w', encoding='utf-8') as fw:
            fw.write(tokenized)

    def tokenize_text(self, txt: str) -> List[Tuple[str, str]]:
        raise NotImplementedError()

    def get_dictionary(self) -> List[str]:
        raise NotImplementedError()


class EnSampleTokenizer(SampleTokenizer):
    def tokenize_text(self, txt: str) -> List[Tuple[str, str]]:
        words = nltk.word_tokenize(txt)
        tokens = nltk.pos_tag(words)
        return tokens

    def get_dictionary(self) -> List[str]:
        from nltk.corpus import words
        pass

from typing import Generator, Type
import regex as re

from vman.apps.vnlp.training.raw_text_processor import RawTextProcessor


class EvaProcessor(RawTextProcessor):
    reg_linenum = re.compile(r"\<[^\>]+\>")

    @classmethod
    def preprocess_text(cls, text: str):
        text = cls.reg_linenum.sub('', text)
        return text

    @classmethod
    def extract_words(cls, text: str, abet: Type) -> Generator[str, None, None]:
        text = cls.preprocess_text(text)
        for w in abet.reg_word.finditer(text):
            word = w.group(0)
            yield word

# -*- coding: utf-8 -*-
import regex as re
from typing import Type, Generator


class RawTextProcessor:
    reg_joins = re.compile(r"'\w|-\w")
    reg_numbers = re.compile(r"\(\w\)|\w\)|\[\w\]|\w\]")
    reg_repeated = re.compile(r"(.)\1{1,}")
    min_word_weight = 0.8

    @classmethod
    def extract_words(cls, text: str, abet: Type) -> Generator[str, None, None]:
        if not text:
            return
        text = text.lower()
        text = text.replace('  ', ' ')
        text = cls.reg_joins.sub('', text)
        text = cls.reg_numbers.sub('', text)
        for w in abet.reg_word.finditer(text):
            word = w.group(0)
            if cls.reg_repeated.match(word):
                continue
            if abet.is_number(word):
                continue
            yield word

    @classmethod
    def process_text(cls, text: str, abet: Type) -> str:
        if not text:
            return ''
        clear_text = ''
        first_item = True
        for word in cls.extract_words(text, abet):
            if not first_item:
                clear_text += ' '
            first_item = False
            clear_text += word

        word_weight = len(clear_text) / len(text)
        if word_weight < cls.min_word_weight:
            return ''
        return clear_text
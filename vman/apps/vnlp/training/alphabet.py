import regex as re


class Alphabet:
    reg_word = re.compile(r'[a-z]+')
    reg_latin_num = re.compile(
        r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$", re.IGNORECASE)

    prefix_max = 3
    prefix_min = 2
    suffix_max = 4
    suffix_min = 1
    root_min = 3

    @classmethod
    def is_number(cls, word: str) -> bool:
        if not cls.reg_latin_num.match(word):
            return False
        if word == 'i':
            return False
        return True


class EnAlphabet(Alphabet):
    pass


class RuAlphabet(Alphabet):
    reg_word = re.compile(r'[абвгдеёжзийклмнопрстуфхцчшщъьэюя]+')


class SlavAlphabet(Alphabet):
    reg_word = re.compile(r'[абвгдеёжзийклмнопрстуфхцчшщъьэюяѣi]+')


alphabet_by_code = {
    'en': EnAlphabet,
    'ru': SlavAlphabet,
    'slav': SlavAlphabet
}

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

    @classmethod
    def preprocess_word(cls, word: str) -> str:
        return word


class EnAlphabet(Alphabet):
    pass


class RuAlphabet(Alphabet):
    reg_word = re.compile(r'[абвгдеёжзийклмнопрстуфхцчшщъыьэюя]+')


class SlavAlphabet(Alphabet):
    reg_word = re.compile(r'[абвгдеёжзийклмнопрстуфхцчшщъыьэюяѣi]+')


class LatinAlphabet(Alphabet):
    reg_word = re.compile(r'[abcdeffhiklmnopqrstvxyz]+')


class GreekAlphabet(Alphabet):
    regular_letters = 'αβγδεζηθικλμνξοπρςστυφχψω'
    reg_word = re.compile(r'[αβγδεζηθικλμνξοπρςστυφχψωϊϋἀἁἂἃἄἅἆἐἑἓἔἕἠἡἢἣἤἥἦἧἰἱἳἴἵἶἷὀὁὂὃὄὅὐὑὒὓὔὕὖὗὠὡὢὣὤὥὦὧὰάὲέὴήὶίὸόὺύὼώᾄᾐᾔᾖᾗᾠᾤᾧᾳᾴᾶᾷῃῄῆῇῒΐῖῥῦῳῴῶῷ]+')
    symbol_map = {
        'ϊ': 'ι', 'ῒ': 'ι', 'ΐ': 'ι', 'ῖ': 'ι', 'ὶ': 'ι', 'ί': 'ι',
        'ϋ': 'ν', 'ὐ': 'ν', 'ὑ': 'ν', 'ὒ': 'ν', 'ὓ': 'ν', 'ὔ': 'ν', 'ὕ': 'ν',
        'ὖ': 'ν', 'ὗ': 'ν', 'ὺ': 'ν', 'ύ': 'ν', 'ῦ': 'ν',
        'ἀ': 'α', 'ἁ': 'α', 'ἂ': 'α', 'ἃ': 'α', 'ἄ': 'α', 'ἅ': 'α', 'ἆ': 'α',
        'ᾄ': 'α', 'ᾳ': 'α', 'ᾴ': 'α', 'ᾶ': 'α', 'ᾷ': 'α', 'ὰ': 'α', 'ά': 'α',
        'ἐ': 'ε', 'ἑ': 'ε', 'ἓ': 'ε', 'ἔ': 'ε', 'ἕ': 'ε', 'ὲ': 'ε', 'έ': 'ε',
        'ἠ': 'η', 'ἡ': 'η', 'ἢ': 'η', 'ἣ': 'η', 'ἤ': 'η', 'ἥ': 'η', 'ἦ': 'η', 'ἧ': 'η',
        'ὴ': 'η', 'ή': 'η', 'ᾐ': 'η', 'ᾔ': 'η', 'ᾖ': 'η', 'ᾗ': 'η', 'ῃ': 'η', 'ῄ': 'η', 'ῆ': 'η', 'ῇ': 'η',
        'ἰ': 'ι', 'ἱ': 'ι', 'ἳ': 'ι', 'ἴ': 'ι', 'ἵ': 'ι', 'ἶ': 'ι', 'ἷ': 'ι',
        'ὀ': 'ο', 'ὁ': 'ο', 'ὂ': 'ο', 'ὃ': 'ο', 'ὄ': 'ο', 'ὅ': 'ο', 'ὸ': 'ο', 'ό': 'ο',
        'ὠ': 'ω', 'ὡ': 'ω', 'ὢ': 'ω', 'ὣ': 'ω', 'ὤ': 'ω', 'ὥ': 'ω', 'ὦ': 'ω', 'ὧ': 'ω', 'ᾠ': 'ω',
        'ᾤ': 'ω', 'ᾧ': 'ω', 'ῳ': 'ω', 'ῴ': 'ω', 'ῶ': 'ω', 'ῷ': 'ω', 'ὼ': 'ω', 'ώ': 'ω',
        'ῥ': 'ρ'
    }

    @classmethod
    def preprocess_word(cls, word: str) -> str:
        result = ''
        for a in word:
            b = cls.symbol_map.get(a) or a
            result += b
        return result


class EvaBasicAlphabetA(Alphabet):
    reg_word = re.compile(r'[\*\'abcdefghijklmnopqrstuvxyz]+')


alphabet_by_code = {
    'en': EnAlphabet,
    'ru': SlavAlphabet,
    'slav': SlavAlphabet,
    'lat': LatinAlphabet,
    'greek': GreekAlphabet,
    'eba': EvaBasicAlphabetA
}

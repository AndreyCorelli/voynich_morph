from unittest import TestCase

from apps.vnlp.tokenization.sample_tokenizer import EnSampleTokenizer


class TestSampleTokenizer(TestCase):
    def test_tokenize(self):
        text = '''The handsome but brutal tribune M. Vinicius, returning to Rome 
        from service in the east, falls in love with "Lygia", a hostage daughter of the Lygian king, 
        who is being raised in the house of Aulus Plautius (a general of British fame), 
        and his wife Pomponia Graecina, who is secretly a Christian.'''

        tokenizer = EnSampleTokenizer()
        output = tokenizer.tokenize_text(text)
        self.assertGreater(len(output), 20)

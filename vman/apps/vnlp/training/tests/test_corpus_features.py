import codecs
import math
import os
from typing import List, Tuple
from unittest import TestCase
from PIL import Image, ImageDraw, ImageColor

from vman.apps.vnlp.training.alphabet import EnAlphabet, SlavAlphabet
from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from vman.apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram
from vman.corpus.corpus_data import RAW_CORPUS_ROOT


class TestCorpusFeatures(TestCase):
    def test_build_corpus_features_en(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        cf = CorpusFeatures('en', EnAlphabet, path_src)
        cf.build()
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)

    def test_build_corpus_features_ru(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'slav')
        cf = CorpusFeatures('slav', SlavAlphabet, path_src)
        cf.build()
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)

    def test_find_morphs(self):
        cf = CorpusFeatures('en', EnAlphabet, '')
        cf.dictionary = DetailedDictionary()
        cf.dictionary.words = [
            WordCard('deprived', 10),
            WordCard('prived', 6),
            WordCard('deprive', 5)
        ]
        cf.dictionary.words_total = len(cf.dictionary.words)
        cf.all_words = {d.word for d in cf.dictionary.words}
        cf.ngrams_collector = MarginNgramsCollector(cf.alphabet, cf.dictionary)
        cf.ngrams_collector.prefixes.append(MarginNgram('de', 1, 3, 1))
        cf.ngrams_collector.prefixes.append(MarginNgram('in', 1, 2, 1))
        cf.ngrams_collector.suffixes.append(MarginNgram('ion', -1, 3, 1))
        cf.ngrams_collector.suffixes.append(MarginNgram('d', -1, 4, 1))
        cf.find_dict_morphs()
        wrd = cf.dictionary.words[0]
        self.assertGreater(len(wrd.root), 0)

    def test_colorize_corpuses(self):
        corpuses = [os.path.join(RAW_CORPUS_ROOT, 'en'),
                    os.path.join(RAW_CORPUS_ROOT, 'slav')]
        alphabets = [EnAlphabet, SlavAlphabet]

        for corp, alph in zip(corpuses, alphabets):
            cf = CorpusFeatures('-', alph, corp)
            cf.build()

            files = [f for f in os.listdir(corp)]
            for file_name in files:
                full_path = os.path.join(corp, file_name)
                if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                    continue
                with codecs.open(full_path, 'r', encoding='utf-8') as fr:
                    text = fr.read()
                words = text.split(' ')
                if not words:
                    continue
                new_file_name = os.path.splitext(full_path)[0]
                new_file_name = new_file_name + '.png'

                vectorized = cf.encode_words_by_morphs(words)
                self.colorize_morph_vectors(new_file_name, vectorized)

    def colorize_morph_vectors(self,
                               out_file_path: str,
                               coded: List[Tuple[float, float, float]]):
        width = 200
        cell_size = 4
        height = math.ceil(len(coded) / width)
        im = Image.new('RGB', (width * cell_size, height * 4), color='black')
        draw = ImageDraw.Draw(im)

        x, y = 0, 0
        f_min = 0
        f_max = max([w[0] for w in coded])
        for freq, pf, sf in coded:
            intense = int(255 * (freq - f_min) / f_max)
            r = intense if pf or not (pf or sf) else 0
            g = intense if sf or not (pf or sf) else 0
            b = intense if not (pf or sf) else 0

            #color = ImageColor.getrgb(f'{r:%02x}{g:%02x}{b:%02x}')
            color = (r, g, b,)
            draw.rectangle([x * cell_size, y * cell_size,
                            (x + 1) * cell_size, (y + 1) * cell_size],
                           fill=color)
            x += 1
            if x >= width:
                x = 0
                y += 1
        im.save(out_file_path)
        del draw



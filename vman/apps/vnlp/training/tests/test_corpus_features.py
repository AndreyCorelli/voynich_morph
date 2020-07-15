import codecs
import math
import os
from typing import List, Tuple
from unittest import TestCase
from PIL import Image, ImageDraw

from apps.vnlp.training.alphabet import EnAlphabet, SlavAlphabet
from apps.vnlp.training.corpus_features import CorpusFeatures
from apps.vnlp.training.detailed_dictionary import DetailedDictionary, WordCard
from apps.vnlp.training.margin_ngrams import MarginNgramsCollector, MarginNgram
from corpus.corpus_data import RAW_CORPUS_ROOT, FEATURES_CORPUS_ROOT, CORPUS_ROOT


class TestCorpusFeatures(TestCase):
    def test_build_corpus_features_en(self):
        path_src = os.path.join(RAW_CORPUS_ROOT, 'en')
        file_name = [f for f in os.listdir(path_src)][0]
        file_path = os.path.join(path_src, file_name)

        dd = DetailedDictionary.read_from_file(file_path)
        cf = CorpusFeatures('en', EnAlphabet, file_path)
        cf.build(dd)
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)

    def test_load_corpus_features_en(self):
        path_src = os.path.join(FEATURES_CORPUS_ROOT, 'en')
        path_src = os.path.join(path_src, 'features.json')
        cf = CorpusFeatures.load_from_file(path_src)
        self.assertGreater(len(cf.ngrams_collector.suffixes), 5)

    def test_build_all_features(self):
        corpus_by_lang = CorpusFeatures.load_from_folder(CORPUS_ROOT)
        self.assertGreater(len(corpus_by_lang), 3)

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
        corpus_by_lang = CorpusFeatures.load_from_folder(CORPUS_ROOT)
        for lang_folder in os.listdir(RAW_CORPUS_ROOT):
            subfolder = os.path.join(RAW_CORPUS_ROOT, lang_folder)
            if not os.path.isdir(subfolder):
                continue
            corpuses = corpus_by_lang[lang_folder]

            files = [f for f in os.listdir(subfolder)]
            for file_name in files:
                full_path = os.path.join(subfolder, file_name)
                if not os.path.isfile(full_path) or not file_name.endswith('.txt'):
                    continue
                with codecs.open(full_path, 'r', encoding='utf-8') as fr:
                    text = fr.read()
                words = text.split(' ')
                if not words:
                    continue

                cf = [c for c in corpuses if c.corpus_path == full_path][0]
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

        # this coeffs make picture more colorful
        colored_intense_min = 90

        for freq, pf, sf in coded:
            f_rel = (freq - f_min) / f_max
            is_gray = not (pf or sf)
            intense_min = 0 if is_gray else colored_intense_min
            intense = int((255 - intense_min) * f_rel) + intense_min

            r = intense if (pf or is_gray) else 0
            g = intense if (sf or is_gray) else 0
            b = intense if is_gray else 0

            r = min(r, 255)
            g = min(g, 255)
            b = min(b, 255)
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



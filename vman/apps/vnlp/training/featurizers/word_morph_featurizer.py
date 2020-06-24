from typing import List, Tuple
from scipy.stats import pearsonr

from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.featurizers.base_featurizer import BaseFeaturizer


class WordMorphFeaturizer(BaseFeaturizer):
    def featurize_words(self, words: List[str], corpus: CorpusFeatures) -> List[float]:
        """
        feature vector consists of:
         - word morphs' frequency correlogramm (xM)
         - word roots' frequency correlogramm (xM)
         - percent of prefix-modified words in the corpus (x1)
         - percent of suffix-modified words in the corpus (x1)
        """
        cw, cr = self.calc_correlations(words, corpus)
        total, words_p, words_s = 0, 0, 0
        for w in corpus.dictionary.words:
            if w.prefix:
                words_p += w.count
            if w.suffix:
                words_s += w.count
            total += w.count

        words_p_rate = words_p / total
        words_s_rate = words_s / total
        return cw + cr + [words_p_rate, words_s_rate]

    def calc_correlations(self,
                          words: List[str],
                          corpus: CorpusFeatures,
                          max_lag: int = 5) -> Tuple[List[float], List[float]]:
        morph_list = []  # type: List[float]
        root_list = []  # type: List[float]

        total = float(sum([w.count for w in corpus.dictionary.words]))
        word_freq = {w.word: w.count / total for w in corpus.dictionary.words}
        root_freq = {w.word: w.root_count / total for w in corpus.dictionary.words}

        for word in words:
            w_freq = word_freq.get(word) or 0
            r_freq = root_freq.get(word) or w_freq
            morph_list.append(w_freq)
            root_list.append(r_freq)
        return self.acf(morph_list, max_lag), self.acf(root_list, max_lag)

    @classmethod
    def acf(cls, lst: List[float], lags_num: int) -> List[float]:
        clm = []  # type: List[float]
        for lag in range(1, lags_num + 1):
            r, _ = pearsonr(lst[lag:], lst[:-lag])[-len(lst):]
            clm.append(r)
        return clm

from typing import List, Tuple, Dict
from scipy.stats import pearsonr

from vman.apps.vnlp.training.corpus_features import CorpusFeatures
from vman.apps.vnlp.training.featurizers.base_featurizer import BaseFeaturizer


class WordMorphFeaturizer(BaseFeaturizer):
    word_freq = {}  # type: Dict[str, float]
    root_freq = {}  # type: Dict[str, float]

    def featurize_words(self, words: List[str], corpus: CorpusFeatures) -> List[float]:
        """
        feature vector consists of:
         - word morphs' frequency correlogramm (xM)
         - word roots' frequency correlogramm (xM)
         - percent of prefix-modified words in the corpus (x1)
         - percent of suffix-modified words in the corpus (x1)
        """
        total = float(sum([w.count for w in corpus.dictionary.words]))
        self.word_freq = {w.word: w.count / total for w in corpus.dictionary.words}
        self.root_freq = {w.word: w.root_count / total for w in corpus.dictionary.words}

        cw, cr = self.calc_correlations(words)
        total, words_p, words_s = 0, 0, 0
        for w in corpus.dictionary.words:
            if w.prefix:
                words_p += w.count
            if w.suffix:
                words_s += w.count
            total += w.count

        words_p_rate = words_p / total
        words_s_rate = words_s / total
        dgram = self.calc_sliding_window_density(words)
        return cw + cr + [words_p_rate, words_s_rate] + dgram

    def calc_correlations(self,
                          words: List[str],
                          max_lag: int = 4) -> Tuple[List[float], List[float]]:
        morph_list = []  # type: List[float]
        root_list = []  # type: List[float]
        for word in words:
            w_freq = self.word_freq.get(word) or 0
            r_freq = self.root_freq.get(word) or w_freq
            morph_list.append(w_freq)
            root_list.append(r_freq)
        return self.acf(morph_list, max_lag), self.acf(root_list, max_lag)

    def calc_sliding_window_density(self, words: List[str], window=10) -> List[float]:
        density = [0] * window
        window_dens = [0] * window

        dmax = 0
        for i in range(0, len(words) - window):
            for j in range(window):
                wf = self.root_freq.get(words[i + j]) or 0
                window_dens[j] = wf
            window_dens.sort(reverse=True)
            for j in range(window):
                density[j] += window_dens[j]
                dmax = max(dmax, density[j])
        d_rel = [d / dmax for d in density]
        return d_rel

    @classmethod
    def acf(cls, lst: List[float], lags_num: int) -> List[float]:
        clm = []  # type: List[float]
        for lag in range(1, lags_num + 1):
            r, _ = pearsonr(lst[lag:], lst[:-lag])[-len(lst):]
            clm.append(r)
        return clm

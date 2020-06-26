from typing import List
from sklearn.ensemble import RandomForestClassifier

from vman.apps.vnlp.training.classifiers.base_classifier import BaseClassifier
from vman.apps.vnlp.training.featurizers.base_featurizer import BaseFeaturizer


class RandomForestLangClassifier(BaseClassifier):
    def __init__(self,
                 featurizer: BaseFeaturizer):
        super().__init__(featurizer)
        self.classifier = RandomForestClassifier()

    def _train(self, x: List[List[float]], y: List[float]):
        self.classifier.fit(x, y)

    def _classify(self, x: List[List[float]]) -> List[float]:
        return self.classifier.predict(x)

    def _classify_vector(self, x: List[List[float]]) -> List[List[float]]:
        probs = self.classifier.predict_proba(x)
        return probs.tolist()

import os
from typing import List
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz

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

    def visualize(self,
                  out_folder: str,
                  featurizer_class):
        estimator = self.classifier.estimators_[5]
        # Export as dot file
        codes = [(self.lang_code[c], c,) for c in self.lang_code]
        codes.sort(key=lambda c: c[0])
        target_names = [c[1] for c in codes]
        feature_names = featurizer_class.get_feature_names()  # type: List[str]

        file_path_dot = os.path.join(out_folder, 'tree.dot')
        file_path_png = os.path.join(out_folder, 'tree.png')
        export_graphviz(estimator,
                        out_file=file_path_dot,
                        feature_names=feature_names,
                        class_names=target_names,
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        from subprocess import call
        call(['dot', '-Tpng', file_path_dot, '-o', file_path_png, '-Gdpi=600'])
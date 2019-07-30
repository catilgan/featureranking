import warnings

from skfeature.function.information_theoretical_based import MRMR as SKF_MRMR
from sklearn import model_selection, svm
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score
from tabulate import tabulate

from fearank.ranking.Ranking import Ranking


class MRMR(Ranking):
    """Ranking with MRMR feature selection method.
    """

    TYPE = "rmrmr"

    @staticmethod
    def get_score(item):
        return item[1]

    @staticmethod
    def execute(data, cols):
        y = data.GroundTruth.values
        x_orig = data.drop(['GroundTruth'], axis=1)
        x = x_orig.values

        clf = svm.LinearSVC()
        num_fea = len(cols)
        fold = model_selection.KFold(n_splits=3, shuffle=True)

        max_acc = 0
        max_idx = None
        max_scores = None
        for train, test in fold.split(x, y):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ConvergenceWarning)
                idx, jcmi, mify = SKF_MRMR.mrmr(x[train], y[train], n_selected_features=num_fea)

                features = x[:, idx[0:num_fea]]

                clf.fit(features[train], y[train])
                y_predict = clf.predict(features[test])

                acc = accuracy_score(y[test], y_predict)

            if acc > max_acc:
                max_acc = acc
                max_idx = idx
                max_scores = jcmi

        headers = ["Name", "Score"]
        values = []
        for i in max_idx[0:num_fea]:
            values.append([x_orig.columns[i], 10 + max_scores[i]])

        sorted_by_score = sorted(values, key=MRMR.get_score, reverse=True)

        return tabulate(sorted_by_score, headers, tablefmt="plain")

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return 'Not implemented!'

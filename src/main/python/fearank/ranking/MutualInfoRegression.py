from sklearn.feature_selection import SelectKBest, mutual_info_regression

from fearank.ranking.Ranking import Ranking


class MutualInfoRegression(Ranking):
    """Select features according to Mutual Info Regression.
    """

    TYPE = 'mutual_info_regression'

    @staticmethod
    def execute(data, cols):
        return Ranking._execute_single(MutualInfoRegression._execute_ranking_sorted, data, cols)

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return Ranking._execute_multiple(MutualInfoRegression._execute_ranking, data, cols, iterations)

    @staticmethod
    def _execute_ranking(x, y):
        model = SelectKBest(score_func=mutual_info_regression, k='all')
        model.fit(x, y)

        idx = list(range(len(model.scores_)))
        return idx, model.scores_

    @staticmethod
    def _execute_ranking_sorted(x, y):
        model = SelectKBest(score_func=mutual_info_regression, k='all')
        model.fit(x, y)

        idx = list(range(len(model.scores_)))
        values = sorted(zip(idx, model.scores_), key=lambda xi: xi[1] * -1)

        idx_sorted = [x[0] for x in values]
        values_sorted = [x[1] for x in values]

        return idx_sorted, values_sorted

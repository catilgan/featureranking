from sklearn.ensemble import ExtraTreesRegressor

from fearank.ranking.Ranking import Ranking


class ExtraTreesRegressorScore(Ranking):
    """An extra-trees regressor."""

    TYPE = "extra_trees_regressor"

    @staticmethod
    def execute(data, cols):
        return Ranking._execute_single(ExtraTreesRegressorScore._execute_ranking_sorted, data, cols)

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return Ranking._execute_multiple(ExtraTreesRegressorScore._execute_ranking, data, cols, iterations)

    @staticmethod
    def _execute_ranking(x, y):
        model = ExtraTreesRegressor(n_jobs=2, n_estimators=1000)
        model.fit(x, y)

        idx = list(range(len(model.feature_importances_)))
        return idx, model.feature_importances_

    @staticmethod
    def _execute_ranking_sorted(x, y):
        model = ExtraTreesRegressor(n_jobs=2, n_estimators=1000)
        model.fit(x, y)

        idx = list(range(len(model.feature_importances_)))
        values = sorted(zip(idx, model.feature_importances_), key=lambda xi: xi[1] * -1)

        idx_sorted = [x[0] for x in values]
        values_sorted = [x[1] for x in values]

        return idx_sorted, values_sorted

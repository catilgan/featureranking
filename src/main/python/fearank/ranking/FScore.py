from skfeature.function.statistical_based import f_score

from fearank.ranking.Ranking import Ranking


class FScore(Ranking):
    """ANOVA F-Score values for Feature Selection

    """

    TYPE = 'f_score'

    @staticmethod
    def execute(data, cols):
        return Ranking._execute_single(FScore._execute_ranking, data, cols)

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return Ranking._execute_multiple(FScore._execute_ranking, data, cols, iterations)

    @staticmethod
    def _execute_ranking(x, y):
        score = f_score.f_score(x, y)
        idx = f_score.feature_ranking(score)
        return idx, score

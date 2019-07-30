from skfeature.function.statistical_based import chi_square

from fearank.ranking.Ranking import Ranking


class ChiSquare(Ranking):
    """Chi-square feature selection
    """

    TYPE = 'chi_square'

    @staticmethod
    def execute(data, cols):
        return Ranking._execute_single(ChiSquare._execute_ranking, data, cols)

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return Ranking._execute_multiple(ChiSquare._execute_ranking, data, cols, iterations)

    @staticmethod
    def _execute_ranking(x, y):
        score = chi_square.chi_square(abs(x), y)
        idx = chi_square.feature_ranking(score)
        return idx, score

import pymrmr

from fearank.ranking.Ranking import Ranking


class MRMRCpp(Ranking):
    """Ranking with MRMR feature selection method using C++ implementation.
    """

    TYPE = "rmrmr_cpp"

    @staticmethod
    def execute(data, cols):
        max_features = len(cols)
        print("====== mRMR Feature Ranking =====")
        ranking = pymrmr.mRMR(data, 'MID', max_features)

        #return ranking
        return '-- Not working --'

    @staticmethod
    def execute_multiple(data, cols, iterations=2):
        return 'Not implemented'

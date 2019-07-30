import abc

from tabulate import tabulate


class Ranking(metaclass=abc.ABCMeta):
    """

    """

    TYPE = 'all'

    @staticmethod
    @abc.abstractmethod
    def execute(data, cols):
        pass

    @staticmethod
    @abc.abstractmethod
    def execute_multiple(data, cols, iterations=2):
        pass

    @staticmethod
    def _get_headers(iterations=1):
        if iterations == 1:
            headers = ["Name", "Score"]
        else:
            headers = ["Name"]
            headers.extend(list(range(1, iterations + 1)))

        return headers

    @staticmethod
    def _tabulate(values, iterations=1):
        headers = Ranking._get_headers(iterations)

        return tabulate(values, headers, tablefmt="plain")

    @staticmethod
    def _execute_single(ranking_func, data, cols):
        y = data.GroundTruth.values
        x_orig = data.drop(['GroundTruth'], axis=1)
        x = x_orig.values
        num_fea = len(cols)

        idx, score = ranking_func(x, y)

        values = []
        for i in idx[0:num_fea]:
            values.insert(i, [x_orig.columns[i], score[i]])

        return Ranking._tabulate(values)

    @staticmethod
    def _execute_multiple(ranking_func, data, cols, iterations=2):
        """

        for each iteration N:
        calculate the scores of the features
        get the indexes of the ranked features
        append the calculated score to the feature iteration values
        return these values

        :param data:
        :param cols:
        :param iterations:
        :return:
        """
        y = data.GroundTruth.values
        x_orig = data.drop(['GroundTruth'], axis=1)
        x = x_orig.values
        num_fea = len(cols)

        scores = {}

        for it in range(iterations):
            idx, score = ranking_func(x, y)

            for i in idx[0:num_fea]:
                if x_orig.columns[i] not in scores:
                    scores[x_orig.columns[i]] = [x_orig.columns[i], score[i]]
                else:
                    scores[x_orig.columns[i]].append(score[i])

        values = list(scores.values())

        return Ranking._tabulate(values, iterations)

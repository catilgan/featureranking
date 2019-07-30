from skfeature.function.information_theoretical_based import FCBF
from skfeature.function.information_theoretical_based import MRMR
from sklearn import svm, model_selection
from sklearn.metrics import accuracy_score
from tabulate import tabulate

from fearank.ranking.Ranking import Ranking


class FastCorrelationBasedFilter(Ranking):
    """Fast Correlation-Based Filter"""
    TYPE = 'fcbf'

    @staticmethod
    def i_execute(data, cols):
        y = data.GroundTruth.values
        x_raw = data.drop(['GroundTruth'], axis=1)
        x = x_raw.values

        f_idx, jcmi, mify = MRMR.mrmr(x, y, n_selected_features=len(cols))
        print(f_idx)
        print(jcmi)
        print(mify)

        headers = ["Name", "Score"]
        values = sorted(zip(x_raw.columns[f_idx], mify), key=lambda xi: xi[1] * -1)

        print(tabulate(values, headers, tablefmt="plain"))

        # headers = ["Name", "Score"]
        # values = sorted(zip(x_train.columns, model.feature_importances_), key=lambda xi: xi[1] * -1)
        #
        # print(tabulate(values, headers, tablefmt="plain"))

    @staticmethod
    def execute(data, cols):
        y = data['GroundTruth'].values
        x_orig = data.drop(['GroundTruth'], axis=1)
        x = x_orig.values

        (idx, uncertainty_idx) = FCBF.fcbf(x, y, n_selected_features=len(cols))

        headers = ["Name", "Score"]
        values = sorted(zip(x_orig.columns[idx], uncertainty_idx), key=lambda xi: xi[1] * -1)

        return tabulate(values, headers, tablefmt="plain")

    @staticmethod
    def _execute(data, cols):
        y = data['GroundTruth'].values
        x = data.drop(['GroundTruth'], axis=1).values

        # split data into 10 folds
        # ss = cross_validation.KFold(n_samples, n_folds=10, shuffle=True)
        ss = model_selection.KFold(n_splits=10, random_state=None, shuffle=True)

        # ss = cross_validate(svc, x, y, cv=10, scoring='accuracy')

        # perform evaluation on classification task
        num_fea = len(cols)  # number of selected features
        clf = svm.LinearSVC()  # linear SVM

        correct = 0
        for train, test in ss.split(x, y):
            # obtain the index of each feature on the training set
            x_train = x[train]
            y_train = y[train]
            (idx, uncertainty_idx) = FCBF.fcbf(x_train, y_train, n_selected_features=num_fea)

            # obtain the dataset on the selected features
            features_idx = idx[0:num_fea]
            features = x[:, features_idx]

            # train a classification model with the selected features on the training dataset
            clf.fit(features[train], y[train])

            # predict the class labels of test data
            y_predict = clf.predict(features[test])

            # obtain the classification accuracy on the test data
            acc = accuracy_score(y[test], y_predict)
            correct = correct + acc

            print(idx, train)
            print(features_idx)
            print(acc)

        # output the average classification accuracy over all 10 folds
        print('Accuracy:', float(correct) / 10)

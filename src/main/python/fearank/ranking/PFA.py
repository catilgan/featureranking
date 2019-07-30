from collections import defaultdict

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import euclidean_distances
from sklearn.preprocessing import StandardScaler


class PFA(object):
    """Feature Selection Using Principal Feature Analysis

    Steps:

        1. Compute the sample covariance matrix,
        2. Compute the Principal components and eigenvalues of the Covariance /Correlation matrix A.
        3. Choose the subspace dimension n, we get new matrix A_n, the vectors Vi are the rows of A_n.
        4. Cluster the vectors |Vi|, using K-Means
        5. For each cluster, find the corresponding vector Vi which is closest to the mean of the cluster.

        Copyright: Sherry Yang
        https://tintinsnowy.com/2018/05/13/feature-selection-for-unsupervised-learning-with-r-and-python/
    """
    def __init__(self, n_features, q=None):
        self.q = q
        self.n_features = n_features
        self.indices_ = []
        self.features_ = []

    def fit(self, X):
        if not self.q:
            self.q = X.shape[1]

        sc = StandardScaler()
        X = sc.fit_transform(X)

        pca = PCA(n_components=self.q).fit(X)
        A_q = pca.components_.T

        kmeans = KMeans(n_clusters=self.n_features).fit(A_q)
        clusters = kmeans.predict(A_q)
        cluster_centers = kmeans.cluster_centers_

        dists = defaultdict(list)
        for i, c in enumerate(clusters):
            dist = euclidean_distances([A_q[i, :]], [cluster_centers[c, :]])[0][0]
            dists[c].append((i, dist))

        self.indices_ = [sorted(f, key=lambda x: x[1])[0][0] for f in dists.values()]
        self.features_ = X[:, self.indices_]

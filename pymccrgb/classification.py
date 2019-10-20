""" Utilities for updating classifcation of point clouds """

from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


def make_sgd_pipeline(
    X_train,
    y_train,
    n_components=1000,
    gamma=0.01,
    alpha=0.0001,
    max_iter=100,
    n_jobs=-1,
    **kwargs
):
    """ Returns an sklearn Pipeline for SGD classification with an RBF kernel

    Parameters
    ----------
        X_train: array
            An n x p array of training examples
        y_train: array
            An n x 1 array of training labels
        n_components: int
            The number of RBF components to use
            (Default: 1000)
        gamma: float
            The gamma/variance parameter of the RBF kernel
            (Default: 0.01)
        alpha: float
            The penalty parameter of the SGD/SVM classifier
            (Default: 0.0001)
        max_iter: int
            The maximum number of iterations to fit the classifier
            (Default: 10)
        n_jobs: int
            The number of jobs to use in fitting the classifier
            (Default: -1, Use all cores)
        Any other keyword argument to sklearn.linear_model.SGDClassifier

    Returns
    -------
        A trained pipeline composed of an RBF transformer and SGD classifier
    """
    estimators = [
        ("rbf", RBFSampler(n_components=n_components, gamma=gamma)),
        ("clf", SGDClassifier(alpha=alpha, n_jobs=n_jobs, max_iter=max_iter, **kwargs)),
    ]
    pipeline = Pipeline(estimators)
    pipeline.fit(X_train, y_train)
    return pipeline

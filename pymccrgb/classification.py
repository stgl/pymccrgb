""" Utilities for updating classifcation of point clouds """

from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

DEFAULT_PARAMETERS = {
    "n_components": 100,
    "gamma": 0.01,
    "alpha": 0.001,
    "max_iter": 100,
    "n_jobs": -1,
}


def make_sgd_pipeline(X_train, y_train, **kwargs):
    """ Returns an sklearn Pipeline for SGD classification with an RBF kernel

    Parameters
    ----------
        X_train: array
            An n x p array of training examples
        y_train: array
            An n x 1 array of training labels
        n_components: int
            The number of RBF components to use
            (Default: 100)
        gamma: float
            The gamma/variance parameter of the RBF kernel
            (Default: 0.01)
        alpha: float
            The penalty parameter of the SGD/SVM classifier
            (Default: 0.001)
        max_iter: int
            The maximum number of iterations to fit the classifier
            (Default: 100)
        n_jobs: int
            The number of jobs to use in fitting the classifier
            (Default: -1, Use all cores)
        Any other keyword argument to sklearn.linear_model.SGDClassifier

    Returns
    -------
        A trained pipeline composed of an RBF transformer and SGD classifier
    """
    if y_train.ndim == 2:
        y_train = y_train.ravel()

    n_components = kwargs.get("n_components", DEFAULT_PARAMETERS["n_components"])
    gamma = kwargs.get("gamma", DEFAULT_PARAMETERS["gamma"])
    alpha = kwargs.get("alpha", DEFAULT_PARAMETERS["alpha"])
    max_iter = kwargs.get("max_iter", DEFAULT_PARAMETERS["max_iter"])
    n_jobs = kwargs.get("n_jobs", DEFAULT_PARAMETERS["n_jobs"])

    estimators = [
        ("rbf", RBFSampler(gamma=gamma, n_components=n_components)),
        ("clf", SGDClassifier(alpha=alpha, n_jobs=n_jobs, max_iter=max_iter)),
    ]
    pipeline = Pipeline(estimators)
    pipeline.fit(X_train, y_train)
    return pipeline

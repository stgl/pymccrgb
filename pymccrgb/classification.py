""" Utilities for updating classifcation of point clouds """

import numpy as np

from copy import copy

from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline


def make_sgd_pipeline(X_train, y_train, max_iter=10, n_jobs=-1, **kwargs):
    estimators = [('rbf', RBFSampler()), ('clf', SGDClassifier(n_jobs=n_jobs, 
                  max_iter=max_iter, **kwargs))]
    pipeline = Pipeline(estimators)
    pipeline.fit(X_train, y_train)
    return pipeline

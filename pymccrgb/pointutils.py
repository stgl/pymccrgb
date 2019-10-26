""" Utilties for common point cloud operations """

import numpy as np
import subprocess

from scipy.spatial import cKDTree


def intersect_rows(arr1, arr2):
    """ Returns a binary mask of the rows in arr1 that are in arr2 """
    mask = np.zeros((arr2.shape[0],), dtype=bool)
    dict1 = {tuple(row): i for i, row in enumerate(arr1)}
    for i, row in enumerate(arr2):
        if tuple(row) in dict1:
            mask[i] = True
    return mask


def point_grid(x_min, x_max, y_min, y_max, dx, dy=None):
    """ Generates a grid of points within a bounding box """
    if dy is None:
        dy = dx
    x = np.arange(x_min, x_max + dx, dx)
    y = np.arange(y_min, y_max + dy, dy)
    X, Y = np.meshgrid(x, y)
    points = np.vstack([X.ravel(), Y.ravel()]).T
    return points


def sample_point_cloud(source, target, sample_indices=[2]):
    """ Resamples a source point cloud at the coordinates of a target points

        Uses the nearest point in the target point cloud to the source point

    Parameters
    ----------
        source: array
            Input point cloud

        target: array
            Target point cloud for sample locations

        sample_indices: list
            List of indices to sample from source. Defaults to 2 (z or height
            dimension)

    Returns
    -------
        An array of sampled points
    """
    sample_indices = np.array(sample_indices)
    tree = cKDTree(source[:, 0:2])
    dist, idx = tree.query(target, n_jobs=-1)
    output = np.hstack(
        [
            target,
            source[idx[:, None], sample_indices].reshape(
                (len(idx), len(sample_indices))
            ),
        ]
    )
    return output


def equal_sample(X, y, size=100, seed=None):
    """ Takes a sample of equal number of feature vectors from each input class

    Assumes y contains discrete labels 0, ..., ymax

    Raises
    ------
        A ValueError if there are insufficient data in a particular class
    """

    if seed is not None:
        np.random.seed(seed)

    Xs = []
    ys = []
    for val in range(y.max() + 1):
        subset = y == val
        if np.sum(subset) < size:
            raise ValueError(
                "Not enough data in class {}: sample size is {}, but only {} data are available".format(
                    val, size, np.sum(subset)
                )
            )
        sample = np.random.choice(np.sum(subset), size=size)
        Xs.append(X[subset][sample, :])
        ys.append(np.full((size, 1), fill_value=val))

    X_sampled = np.vstack(Xs)
    y_sampled = np.vstack(ys)

    return X_sampled, y_sampled


def stratified_sample(X, y, size=100, seed=None):
    """ Takes a stratified sample of feature vectors from each input class

    Assumes y contains discrete labels 0, ..., ymax

    Raises
    ------
        A ValueError if there are insufficient data in a particular class
    """

    if seed is not None:
        np.random.seed(seed)

    Xs = []
    ys = []
    for val in range(y.max() + 1):
        subset = y == val
        frac = np.sum(subset) / len(y)
        target_size = int(frac * size)

        if np.sum(subset) < target_size:
            raise ValueError(
                "Not enough data in class {}: sample size is {}, but {} data are available".format(
                    val, size, np.sum(subset)
                )
            )
        sample = np.random.choice(np.sum(subset), size=target_size)
        Xs.append(X[subset][sample, :])
        ys.append(np.full((target_size, 1), fill_value=val))

    X_sampled = np.vstack(Xs)
    y_sampled = np.vstack(ys)

    return X_sampled, y_sampled

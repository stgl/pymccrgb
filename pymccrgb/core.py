""" MCC lidar classification with color clustering """

import numpy as np

from copy import copy

from classification import make_sgd_pipeline 
from features import calculate_color_features
from plotting import plot_results
from utils import equal_sample

from pymcc_lidar import pymcc_singlepass as calculate_excess_height


def classify_ground_mcc(data, scale, tol, downsample=False):
    """ Classifies ground points by a single iteration of the MCC algorithm

    Classifies ground and nonground (or "high") points by comparing the
    elevation of each data point to an interpolated surface. If downsample is
    True, a down-sampled version of the data coordinates will be used when
    interpolating (currently not implemented).

    Args:
        data: A n x 3 (or more) data matrix with rows [x, y, z, ...]
        scale: The interpolation scale. This defines the resolution of the
            interpolated surface, which is calculated by a 3 x 3 windowed
            mean around each intrpolation point.
        tol: The height tolerance. Points exceeding the durface by more than
            tol units are classified as nonground
        downsample: If True, use a downsampled dataset for interpolation.
            Not implemented.

    Returns:
        An n x 1 array of point class labels. 1 is ground, and 0 is nonground.
    """
    xyz = data[:, 0:3]
    height = calculate_excess_height(xyz.copy(order='C'), scale)
    y = (height < tol)  # 0 = nonground, 1 = ground
    return y


def mcc(data,
        scales=[0.5, 1, 1.5],
        tols=[0.3, 0.3, 0.3],
        threshs=[1, 0.1, 0.01]):
    """ Classifies ground points using the MCC algorithm

    Classifies ground and nonground (or "high") points by comparing the
    elevation of each data point to an interpolated surface at user-defined
    scales. The algorithm iterates at each scale until a convergence threshold
    is reached based on the percentage of points classified as ground. Only
    ground points are retained after each iteration.

    Args:
        data: A n x d data matrix with rows [x, y, z, ...]
        scales: The interpolation scales. This defines the resolution of the
            interpolated surface, which is calculated by a 3 x 3 windowed
            mean around each intrpolation point. Defaults to [0.5, 1, 1.5]
            meters.
        tols: The height tolerances. Points exceeding the durface by more than
            tol units are classified as nonground. Deaults to 0.3 meters.
        threshs: The convergence thresholds as percentages. Defaults to
            [1%, 0.1%, 0.01%]

    Returns:
        An m x d array of ground points
    """

    for scale, tol, thresh in zip(scales, tols, threshs):
        converged = False
        niter = 0
        while not converged:
            n_points = data.shape[0]
            y = classify_ground_mcc(data, scale, tol)
            ground = y == 1
            n_removed = np.sum(y == 0)
            converged = 100 * (n_removed / n_points) < thresh
            data = data[ground, :]
            print('-' * 20)
            print('SD: {:.2f}, tol: {:.1e}, iter: {}'.format(scale, tol, niter))
            print('Removed {} nonground points ({:.2f} %)'.format(n_removed, 100 * (n_removed / n_points)))
            niter += 1
    return data


def mcc_rgb(data,
            scales=[0.5, 1, 1.5],
            tols=[0.3, 0.3, 0.3],
            threshs=[1, 0.1, 0.01],
            training_scales=None,
            training_tols=None,
            n_train=int(1e5)):
    """ Classifies ground points using the MCC-RGB algorithm

    Classifies ground and nonground (or "high") points by comparing the
    elevation of each data point to an interpolated surface at user-defined
    scales. The algorithm proceeds as MCC (see the mcc() documentation), except 
    that ground points are reclassified based on their color similarity to
    nonground points.

    Args:
        data: A n x d data matrix with rows [x, y, z, r, g, b ...]
        scales: The interpolation scales. This defines the resolution of the
            interpolated surface, which is calculated by a 3 x 3 windowed
            mean around each intrpolation point. Defaults to [0.5, 1, 1.5]
            meters.
        tols: The height tolerances. Points exceeding the durface by more than
            tol units are classified as nonground. Deaults to 0.3 meters.
        threshs: The convergence thresholds as percentages. Defaults to
            [1%, 0.1%, 0.01%]
        training_scales: The interpolation scales. This defines the resolution of the
            interpolated surface, which is calculated by a 3 x 3 windowed
            mean around each intrpolation point. Defaults to [0.5, 1, 1.5]
            meters.
        training_tols: The height tolerances. Points exceeding the durface by more than
            tol units are classified as nonground. Deaults to 0.3 meters.
        n_train: The number of points to use for training the color classifier
            Defaults to 1E5

    Returns:
        data: An m x d array of ground points
        updated: An n x 1 array of labels indicating whether the point was
            updated in an MCC-RGB step. If there are multiple training scales,
            this will be the index of the scale and tolerance range defined
            in training_scales and training_tols. (Currently implemented for
            only one update scale/tolerance, with 0 being not updated, and 1
            updated).
    """

    if training_scales is None:
        training_scales = scales[0:1]

    if training_tols is None:
        training_tols = tols[0:1]
     
    for scale, tol, thresh in zip(scales, tols, threshs):
        converged = False
        niter = 0
        while not converged:
            n_points = data.shape[0]
            y = classify_ground_mcc(data, scale, tol)
            n_removed_mcc = np.sum(y == 0)

            print('-' * 20)
            print('SD: {:.2f}, tol: {:.1e}, iter: {}'.format(scale, tol, niter))
            print('Removed {} nonground points in MCC ({:.2f} %)'.format(n_removed_mcc, 100 * (n_removed_mcc / n_points)))

            if scale == scales[0] and niter == 0:
                X = calculate_color_features(data)
                X_train, y_train = equal_sample(X, y, size=int(n_train / 2))
                pipeline = make_sgd_pipeline(X_train, y_train)
                y_pred = pipeline.predict(X)

                n_removed_clf = np.sum((y == 1) & (y_pred == 0))
                updated = (y == 1) & (y_pred == 0)
                y[updated] = 0

                print('Removed {} nonground points in update step ({:.2f} %)'.format(n_removed_clf, 100 * (n_removed_clf / n_points)))
                
            ground = y == 1
            n_removed = np.sum(y == 0)
            converged = 100 * (n_removed / n_points) < thresh

            data = data[ground, :]
            niter += 1
    return data, updated

""" Multiscale curvature classification of ground points with color updates """

import numpy as np

from classification import make_sgd_pipeline
from features import calculate_color_features
from utils import equal_sample

from pymcc_lidar import pymcc_singlepass as calculate_excess_height


def classify_ground_mcc(data, scale, tol, downsample=False):
    """ Classifies ground points by a single iteration of the MCC algorithm

    Classifies ground and nonground (or "high") points by comparing the
    elevation of each data point to an interpolated surface. If downsample is
    True, a down-sampled version of the data coordinates will be used when
    interpolating (currently not implemented).

    Based on MCC algorithm implemented in [1, 2].

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

    References:
        [1] Evans, Jeffrey S.; Hudak, Andrew T. 2007. A multiscale curvature
            algorithm for classifying discrete return LiDAR in forested
            environments. Geoscience and Remote Sensing. 45(4): 1029-1038.
        [2] https://sourceforge.net/p/mcclidar
    """
    xyz = data[:, 0:3]
    height = calculate_excess_height(xyz.copy(order='C'), scale)
    y = (height < tol)  # 0 = nonground, 1 = ground
    return y


def mcc(data,
        scales=[0.5, 1, 1.5],
        tols=[0.3, 0.3, 0.3],
        threshs=[1, 0.1, 0.01],
        verbose=False):
    """ Classifies ground points using the MCC algorithm

    Classifies ground and nonground (or "high") points by comparing the
    elevation of each data point to an interpolated surface at user-defined
    scales. The algorithm iterates at each scale until a convergence threshold
    is reached based on the percentage of points classified as ground. Only
    ground points are retained after each iteration.

    Based on MCC algorithm implemented in [1, 2].

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

    References:
        [1] Evans, Jeffrey S.; Hudak, Andrew T. 2007. A multiscale curvature
            algorithm for classifying discrete return LiDAR in forested
            environments. Geoscience and Remote Sensing. 45(4): 1029-1038.
        [2] https://sourceforge.net/p/mcclidar
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

            if verbose:
                print('-' * 20)
                print('MCC iteration')
                print('-' * 20)
                print('Scale: {:.2f}, Relative height: {:.1e}, iter: {}'.format(scale, tol, niter))
                print('Removed {} nonground points ({:.2f} %)'.format(n_removed, 100 * (n_removed / n_points)))

            niter += 1
    return data


def mcc_rgb(data,
            scales=[0.5, 1, 1.5],
            tols=[0.3, 0.3, 0.3],
            threshs=[1, 0.1, 0.01],
            training_scales=None,
            training_tols=None,
            n_train=int(1e5),
            max_iter=20,
            verbose=False):
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
            mean around each interpolation point. Defaults to [0.5, 1, 1.5]
            meters. Scale domains are processed in order of increasing scale.

        tols: The height tolerances. Points exceeding the surface by more than
            tol units are classified as nonground. Deaults to 0.3 meters.

        threshs: The convergence thresholds as percentages. Defaults to
            [1%, 0.1%, 0.01%]

        training_scales: The training interpolation scales.
            This defaults to the first scale domain (e.g., 0.5). Both
            training_scales and training_tols must be specified;
            otherwise the defaults are used.

        training_tols: The training relative heights. Defaults to the first
            height tolerance (e.g., 0.3). Both training_scales and
            training_tols must be specified; otherwise the defaults are used.

        n_train: The total number of points to use for training the color
            classifier. Defaults to 1E5.

        max_iter: Maximum number of iterations in a scale domain.
            Defaults to 20.

    Returns:
        data: An m x d array of ground points

        updated: An n x 1 array of labels indicating whether the point was
            updated in an MCC-RGB step. -1 indicates the point's classification
            was not updated. If there are multiple training scales,
            this will be the index of the scale and tolerance range defined
            in training_scales and training_tols.
    """

    if training_scales is None or training_tols is None:
        training_tols = tols[0:1]
        training_scales = scales[0:1]
    else:
        scales += training_scales
        tols += training_tols
        idx = np.argsort(scales)
        scales = scales[idx]
        tols = tols[idx]

    n_points = data.shape[0]
    updated = np.full((n_points,), fill_value=-1)
    reached_max_iter = False

    for scale, tol, thresh in zip(scales, tols, threshs):
        converged = False
        niter = 0
        while not converged and not reached_max_iter:
            y = classify_ground_mcc(data, scale, tol)

            if verbose:
                n_removed_mcc = np.sum(y == 0)
                print('-' * 20)
                print('MCC step')
                print('-' * 20)
                print('Scale: {:.2f}, Relative height: {:.1e}, iter: {}'.format(scale, tol, niter))
                print('Removed {} nonground points ({:.2f} %)'.format(n_removed_mcc, 100 * (n_removed_mcc / n_points)))

            update_step = scale in training_scales and tol in training_tols
            first_iter = niter == 0
            if update_step and first_iter:
                X = calculate_color_features(data)
                X_train, y_train = equal_sample(X, y, size=int(n_train / 2))
                pipeline = make_sgd_pipeline(X_train, y_train)
                y_pred = pipeline.predict(X)

                params = list(zip(training_scales, training_tols))
                update_step_idx = params.index((scale, tol))
                updated[(y == 1) & (y_pred == 0)] = update_step_idx
                y[(y == 1) & (y_pred == 0)] = 0

                if verbose:
                    n_removed_clf = np.sum((y == 1) & (y_pred == 0))
                    print('-' * 20)
                    print('Classification update step')
                    print('-' * 20)
                    print('Scale: {}, Relative height: {}'.format(scale, tol))
                    print('Removed {} nonground points ({:.2f} %)'.format(n_removed_clf, 100 * (n_removed_clf / n_points)))

            ground = y == 1
            data = data[ground, :]

            n_removed = np.sum(y == 0)
            converged = 100 * (n_removed / n_points) < thresh
            reached_max_iter = niter >= max_iter

            niter += 1
    return data, updated

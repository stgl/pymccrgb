"""
Calculate indices and other features from multi-channel point cloud data

Inputs are assumed to be n x 6 arrays with each row being x, y, z, r, g, b
"""

import numpy as np

from skimage.color import rgb2lab, rgb2hsv
from skimage.exposure import rescale_intensity





def calculate_eigenvalue_features(data):
    raise NotImplementedError("This method has not yet been implemented.")


def calculate_ngrdvi(data):
    """ Calculates red-green difference index (NGRDVI) from color data

    Parameters
    ----------
        data: array
        An n x d array of input data. Rows are [x, y, z, r, g, b, ...]

    Returns
    -------
        An n x 1 array of NGRDVI values
    """

    rgb = rescale_intensity(data[:, 3:6], out_range="uint8").astype(np.uint8)
    red = rgb[:, 0].reshape(-1, 1)
    green = rgb[:, 1].reshape(-1, 1)

    return (green - red) / (green + red)

def calculate_hue(data):
    """ Calculates hsv from color data

    Parameters
    ----------
        data: array
        An n x d array of input data. Rows are [x, y, z, r, g, b, ...]

    Returns
    -------
        An n x 1 array of h values
    """

    rgb = rescale_intensity(data[:, 3:6], out_range="uint8").astype(np.uint8)
    hsv = rgb2hsv(np.array([rgb]))[0].reshape(-1,3)
    hue = hsv[:,0].reshape(-1,1)

    return hue

def calculate_color_features(data, color_model = calculate_ngrdvi):
    """ Calculates color features related to the greenness of each point.

    The default features are [a, b, NGRDVI] where a and b are the green-red and
    blue-yellow coordinates of the CIE-Lab color space.

    Parameters
    ----------
        data: array
        An n x d array of input data. Rows are [x, y, z, r, g, b, ...]

    Returns
    -------
        An n x 3 array of features for each point.
    """

    rgb = rescale_intensity(data[:, 3:6], out_range="uint8").astype(np.uint8)
    lab = rgb2lab(np.array([rgb]))[0].reshape(-1, 3)
    color_variable = color_model(data).reshape(-1, 1)
    return np.hstack([lab[:, 1:3], color_variable])

def calculate_vdvi(data):
    """ Calculates visual difference vegetation index (VDVI) from color data

    Parameters
    ----------
        data: array
        An n x d array of input data. Rows are [x, y, z, r, g, b, ...]

    Returns
    -------
        An n x 1 array of VDVI values
    """

    rgb = rescale_intensity(data[:, 3:6], out_range="uint8").astype(np.uint8)
    red = rgb[:, 0].reshape(-1, 1)
    green = rgb[:, 1].reshape(-1, 1)
    blue = rgb[:, 2].reshape(-1, 1)

    return (2 * green - red - blue) / (2 * green + red + blue)

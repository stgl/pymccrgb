"""
Calculate indices and other features from multi-channel point cloud data

Inputs are assumed to be n x 6 arrays with each row being x, y, z, r, g, b
"""

import numpy as np

from scipy.misc import bytescale
from skimage.color import rgb2lab


def calculate_ngrdvi(data):
    red = data[:, 3]
    green = data[:, 4]

    return (green - red) / (green + red)


def calculate_vdvi(data):
    red = data[:, 3]
    green = data[:, 4]
    blue = data[:, 5]

    return (2 * green - red - blue) / (2 * green + red + blue)


def calculate_color_features(data):
    rgb = bytescale(data[:, 3:6]).astype(np.int16)
    lab = rgb2lab(np.array([rgb]))[0].reshape(-1,3)
    ngrdvi = calculate_ngrdvi(data).reshape(-1,1)
    return np.hstack([lab[:, 1:3], ngrdvi])

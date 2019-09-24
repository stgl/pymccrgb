""" Load example datasets of lidar and photogrammetric point clouds """

import os

from .ioutils import load_las

directories = os.path.dirname(__file__)
path = "/".join(directories.split("/")[0:-1])
DATA_DIRECTORY = os.path.join(path, "docs/source/examples/data")


def load_kaibab_lidar(npoints=None):
    """Loads sample dataset from Kaibab Plateau, Arizona, USA lidar dataset

    Parameters
    ----------
        npoints: int
            Optional number of (random) points to load from file

    Returns
    -------
        A data ndarray
    """
    filename = os.path.join(DATA_DIRECTORY, "kaibab_lidar.laz")
    data = load_las(filename, nrows=npoints)
    return data


def load_mammoth_lidar(npoints=None):
    """Loads sample dataset from Mammoth Mountain, California, USA lidar dataset

    Parameters
    ----------
        npoints: int
            Optional number of (random) points to load from file

    Returns
    -------
        A data ndarray
    """
    filename = os.path.join(DATA_DIRECTORY, "mammoth_lidar.laz")
    data = load_las(filename, nrows=npoints)
    return data


def load_mammoth_sfm(npoints=None):
    """Loads sample dataset from Mammoth Mountain, California, USA structure-from-motion dataset

    Parameters
    ----------
        npoints: int
            Optional number of (random) points to load from file

    Returns
    -------
        A data ndarray
    """
    filename = os.path.join(DATA_DIRECTORY, "mammoth_sfm.laz")
    data = load_las(filename, nrows=npoints)
    return data

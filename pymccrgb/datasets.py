""" Load example datasets of lidar and photogrammetric point clouds """

import os

from urllib.request import urlretrieve

from .ioutils import read_las

path = os.path.dirname(__file__)
LOCAL_DATA_PATH = os.path.join(path, "data")
REMOTE_DATA_URL = "https://pymccrgb-data.s3-us-west-2.amazonaws.com/"


def load_dataset(filename, npoints=None):
    """Loads sample dataset from an S3 bucket

    Parameters
    ----------
        filename: str
            Filename of remote/local file
        npoints: int
            Optional number of (random) points to load from file

    Returns
    -------
        A data ndarray
    """
    if not filename.endswith((".las", ".laz")):
        raise ValueError(
            "Data file must be in LAS or LAZ format (.las, .laz)."
            "You provided the file " + filename
        )
    if not os.path.exists(LOCAL_DATA_PATH):
        os.mkdir(LOCAL_DATA_PATH)

    local_filename = os.path.join(LOCAL_DATA_PATH, filename)
    if not os.path.exists(local_filename):
        url = os.path.join(REMOTE_DATA_URL, filename)
        urlretrieve(url, local_filename)

    data = read_las(local_filename, nrows=npoints)
    return data


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
    raise NotImplementedError("This sample dataset is not available yet!")
    # data = load_dataset("kaibab_lidar.laz", npoints=npoints)
    # return data


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
    data = load_dataset("mammoth_lidar.laz", npoints=npoints)
    return data


def load_mammoth_sfm(npoints=None):
    """Loads sample dataset from Mammoth Mountain, California, USA
    structure-from-motion dataset

    Parameters
    ----------
        npoints: int
            Optional number of (random) points to load from file

    Returns
    -------
        A data ndarray
    """
    raise NotImplementedError("This sample dataset is not available yet!")
    # data = load_dataset("mammoth_sfm.laz", npoints=npoints)
    # return data

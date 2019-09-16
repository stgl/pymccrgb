""" Load example datasets of lidar and photogrammetric point clouds """

import os

from io import load_txt

directories = os.path.dirname(__file__)
path = "/".join(directories.split("/")[0:-1])
DATA_DIRECTORY = os.path.join(path, "docs/source/examples/data")


def load_kaibab_lidar(npoints=None):
    raise NotImplementedError("This method has not yet been implemented.")


def load_mammoth_lidar(npoints=None):
    filename = os.path.join(DATA_DIRECTORY, "mammoth_lidar'txt")
    data = load_txt(filename, nrows=npoints)
    return data


def load_mammoth_sfm(npoints=None):
    raise NotImplementedError("This method has not yet been implemented.")

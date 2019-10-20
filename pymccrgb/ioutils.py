""" Convenience functions for loading point clouds in various formats """

import os

import numpy as np
import pdal

DEFAULT_COLUMN_INDICES = range(6)
DEFAULT_COLUMN_NAMES = ["X", "Y", "Z", "Red", "Green", "Blue"]
DEFAULT_HEADER = "X,Y,Z,Red,Green,Blue"


def read_data(filename, usecols=None, userows=None, nrows=None):
    """ Loads a point cloud as numpy array

    Parameters
    ----------
        filename: str
            Filename of text file containing point cloud

        usecols: list
            List of column indices (text file) or names (LAS file) to load
            Default: First six columns, e.g.,  (x, y, z, r, g, b)

        userows: list
            List of rows to load. Overrides nrows argument
            Default: All rows

        nrows: int
            Number of random rows to load. Ignored if userows is given.
            Default: Not used.

    Returns
    -------
        A data array of shape (nrows x ncols)
    """
    if filename.endswith(".csv") or filename.endswith(".txt"):
        if usecols is None:
            usecols = DEFAULT_COLUMN_INDICES
        data = read_txt(filename, usecols=usecols, userows=userows, nrows=nrows)
    elif filename.endswith(".las") or filename.endswith(".laz"):
        if usecols is None:
            usecols = DEFAULT_COLUMN_NAMES
        data = read_las(filename, usecols=usecols, userows=userows, nrows=nrows)
    else:
        raise ValueError(
            "Unsupported format provided. Please provide a CSV file"
            "(.txt or .csv) or LAS/LAZ file."
        )
    return data


def read_txt(filename, usecols=DEFAULT_COLUMN_INDICES, userows=None, nrows=None):
    """ Loads a point cloud from text file as numpy array

    Parameters
    ----------
        filename: str
            Filename of text file containing point cloud

        usecols: list
            List of column indices to load
            Default: First six columns, e.g.,  (x, y, z, r, g, b)

        userows: list
            List of rows to load. Overrides nrows argument
            Default: All rows

        nrows: int
            Number of random rows to load. Ignored if userows is given.
            Default: Not used.

    Returns
    -------
        A data array of shape (nrows x ncols)
    """

    if userows is None:
        with open(filename, "r") as f:
            for i, s in enumerate(f):
                pass
        nlines = i + 1
        if nrows is not None:
            nrows = int(nrows)
            userows = np.random.choice(nlines, size=nrows)
        else:
            userows = range(nlines)

    data = []
    with open(filename, "r") as f:
        for i, s in enumerate(f):
            if i in userows:
                row = s.split(",")
                row = np.asarray(row)
                row = row[usecols]
                data.append(row)
    return np.array(data)


def read_las(filename, usecols=DEFAULT_COLUMN_NAMES, userows=None, nrows=None):
    """Loads a point cloud from a LAS or LAZ file into a Numpy array

    Theoretically, any file with a PDAL reader can be read with read_las

    Parameters
    ----------
        filename: str
            Filename of LAS or LAZ file containing point cloud

        usecols: list
            List of column names to load
            Default: ['X', 'Y', 'Z', 'Red', 'Green', 'Blue']

        userows: list
            List of rows to load. Overrides nrows argument
            Default: All rows

        nrows: int
            Number of random rows to load. Ignored if userows is given.
            Default: Not used.

    Returns
    -------
        A data array of shape (nrows x ncols)
    """

    json = '{"pipeline": ["' + filename + '"]}'
    pipeline = pdal.Pipeline(json)
    pipeline.validate()
    pipeline.loglevel = 0
    _ = pipeline.execute()

    out = pipeline.arrays[0]
    if userows is None:
        if nrows is None:
            data = np.hstack([out[key].reshape(-1, 1) for key in usecols])
            return data
        nrows = int(nrows)
        userows = np.random.choice(out.shape[0], size=nrows)

    data = []
    for i in userows:
        point = []
        for key in usecols:
            point.append(out[key][i])
        data.append(point)

    ncols = len(usecols)
    data = np.array(data).reshape(nrows, ncols)

    return data


def write_dem(data, filename, resolution=1, radius=None):
    if radius is None:
        radius = resolution * np.sqrt(2)

    write_las(data, "temp.las")

    json = (
        '{"pipeline": [{"type": "readers.las", "filename": "temp.las"}, {"type": "writers.gdal", "resolution": "'
        + str(resolution)
        + '", "radius": "'
        + str(radius)
        + '", "filename": "'
        + filename
        + '"}]}'
    )
    pipeline = pdal.Pipeline(json)
    pipeline.validate()
    pipeline.loglevel = 0
    _ = pipeline.execute()

    os.remove("temp.las")


def write_las(arr, filename):
    write_pdal(arr, filename, writer="writers.las")


def write_pdal(arr, filename, writer, header=DEFAULT_HEADER):
    np.savetxt("temp.csv", arr, header=header, delimiter=",", comments="")

    json = (
        '{"pipeline": [{"type": "readers.text", "filename": "temp.csv"}, {"type": "'
        + writer
        + '", "filename": "'
        + filename
        + '"}]}'
    )
    pipeline = pdal.Pipeline(json)
    pipeline.validate()
    pipeline.loglevel = 0
    _ = pipeline.execute()

    os.remove("temp.csv")

""" Convenience functions for loading point clouds in various formats """

import numpy as np
import pdal

DEFAULT_COLUMNS = ["X", "Y", "Z", "Red", "Green", "Blue"]


def load_txt(filename, usecols=range(6), userows=None, nrows=None):
    """ Loads specified rows and columns from text file as numpy array

    Args:
        filename: Filename of text file containing point cloud

        usecols: List of column indices to load
            Default: First six columns, e.g.,  (x, y, z, r, g, b)

        userows: List of rows to load. Overrides nrows argument
            Default: All rows

        nrows: Number of random rows to load. Ignored if userows is given.
            Default: Not used.

    Returns: A data array of shape (nrows x ncols)
    """

    if userows is None:
        with open(filename, "r") as f:
            for i, s in enumerate(f):
                pass
        nlines = i + 1
        if nrows is not None:
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


def load_las(filename, userows=None, usecols=DEFAULT_COLUMNS):
    json = '{"pipeline": ["' + filename + '"]}'
    pipeline = pdal.Pipeline(json)
    pipeline.validate()
    pipeline.loglevel = 0
    nrows = pipeline.execute()

    out = pipeline.arrays[0]
    if userows is None:
        data = np.hstack([out[key].reshape(-1, 1) for key in usecols])
    else:
        nrows = out.shape[0]
        userows = range(nrows)

        data = []
        for i in userows:
            point = []
            for key in usecols:
                point.append(out[key][i])
            data.append(point)

        ncols = len(usecols)
        data = np.array(data).reshape(nrows, ncols)

    return data

""" Test computing color features from point cloud """

import os

import pytest
import unittest

import numpy as np

from context import pymccrgb

from pymccrgb import features, ioutils

TEST_DIR = os.path.dirname(__file__)

# Indices of derived features in test data
L_INDEX = 0
A_INDEX = 1
B_INDEX = 2
NGRDVI_INDEX = 3
VDVI_INDEX = 4
DEFAULT_FEATURE_INDEXES = [A_INDEX, B_INDEX, NGRDVI_INDEX]


class ColorFeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.data = ioutils.load_las(os.path.join(TEST_DIR, "points_rgb.laz"))
        self.target = np.load(os.path.join(TEST_DIR, "features_rgb.npy"))

    def test_calculate_color_features(self):
        test = features.calculate_color_features(self.data)
        true = self.target[:, DEFAULT_FEATURE_INDEXES]
        self.assertTrue(
            np.allclose(test, true),
            "Default color feature calculation (a, b, NGRDVI) is incorrect",
        )

    def test_calculate_ngrdvi(self):
        test = features.calculate_ngrdvi(self.data)
        true = self.target[:, NGRDVI_INDEX]
        self.assertTrue(np.allclose(test, true), "NGRDVI calculation is incorrect")

    def test_calculate_vdvi(self):
        test = features.calculate_vdvi(self.data)
        true = self.target[:, VDVI_INDEX]
        self.assertTrue(np.allclose(test, true), "VDVI calculation is incorrect")

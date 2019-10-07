""" Test computing color features from point cloud """

import os

import pytest
import unittest

import numpy as np

from context import pymccrgb

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

# Indices of derived features in test data
L_INDEX = 0
A_INDEX = 1
B_INDEX = 2
NGRDVI_INDEX = 3
VDVI_INDEX = 4
DEFAULT_FEATURE_INDEXES = [A_INDEX, B_INDEX, NGRDVI_INDEX]


class ColorFeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.data = pymccrgb.ioutils.read_las(
            os.path.join(TEST_DATA_DIR, "points_rgb.laz")
        )
        self.target = np.load(os.path.join(TEST_OUTPUT_DIR, "features_rgb.npy"))

    def test_calculate_color_features(self):
        test = pymccrgb.features.calculate_color_features(self.data)
        true = self.target[:, DEFAULT_FEATURE_INDEXES]
        self.assertTrue(
            np.allclose(test, true),
            "Default color feature calculation (a, b, NGRDVI) is incorrect",
        )

    def test_calculate_ngrdvi(self):
        test = pymccrgb.features.calculate_ngrdvi(self.data)
        test = test[np.isfinite(test)]
        true = self.target[:, NGRDVI_INDEX]
        true = true[np.isfinite(true)]
        self.assertTrue(np.allclose(test, true), "NGRDVI calculation is incorrect")

    def test_calculate_vdvi(self):
        test = pymccrgb.features.calculate_vdvi(self.data)
        test = test[np.isfinite(test)]
        true = self.target[:, VDVI_INDEX]
        true = true[np.isfinite(true)]
        self.assertTrue(np.allclose(test, true), "VDVI calculation is incorrect")

""" Test Python MCC bindings and MCC-RGB algorithm """

import os

import pytest
import unittest

import numpy as np

from context import pymccrgb

TEST_DIR = os.path.dirname(__file__)
TEST_SCALES = [0.5, 1, 1.5]
TEST_TOLS = [0.01, 0.05, 0.3, 0.5, 1]


class MCCTestCase(unittest.TestCase):
    def setUp(self):
        self.data = pymccrgb.ioutils.load_las(os.path.join(TEST_DIR, "points_rgb.laz"))

    def _test_classify_ground_mcc(self, scale, tol):
        test = pymccrgb.core.classify_ground(self.data, scale, tol)
        true = np.load(os.path.join(TEST_DIR, f"classification_mcc_{scale}_{tol}.npy"))
        self.assertEqual(
            test,
            true,
            f"MCC ground classification is incorrect for scale {scale} and height tolerance {tol}",
        )

    def test_mcc_classification(self):
        for scale in TEST_SCALES:
            for tol in TEST_TOLS:
                self._test_classify_ground_mcc(scale, tol)

    def test_mcc_default(self):
        test_points, test_labels = pymccrgb.core.mcc(self.data, verbose=True)
        true_points, true_labels = np.load(
            os.path.join(TEST_DIR, f"ground_labels_mcc_default.npy")
        )
        self.assertTrue(
            np.allclose(test_points, true_points),
            "Ground points are incorrect for default MCC configuration",
        )
        self.assertTrue(
            np.allclose(test_labels, true_labels),
            "Classification is incorrect for default MCC configuration",
        )


class MCCRGBTestCase(unittest.TestCase):
    def setUp(self):
        self.data = pymccrgb.ioutils.load_las(os.path.join(TEST_DIR, "points_rgb.laz"))

    def test_mcc_rgb_default(self):
        test_points, test_labels = pymccrgb.core.mcc_rgb(self.data, verbose=True)
        true_points, true_labels, true_updated = np.load(
            os.path.join(TEST_DIR, f"ground_labels_mc_crgb_default.npy")
        )
        self.assertTrue(
            np.allclose(test_points, true_points),
            "Ground points are incorrect for default MCC-RGB configuration",
        )
        self.assertTrue(
            np.allclose(test_labels, true_labels),
            "Classification is incorrect for default MCC-RGB configuration",
        )
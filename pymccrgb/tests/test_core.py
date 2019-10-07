""" Test Python MCC bindings and MCC-RGB algorithm """

import os

import pytest
import unittest

import numpy as np

from context import pymccrgb

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

TEST_SCALES = [0.5, 1.0, 1.5]
TEST_TOLS = [0.01, 0.05, 0.3, 0.5, 1.0]
SEED_VALUE = 42


class MCCTestCase(unittest.TestCase):
    def setUp(self):
        self.data = pymccrgb.ioutils.read_las(
            os.path.join(TEST_DATA_DIR, "points_rgb.laz")
        )

    def _test_classify_ground_mcc(self, scale, tol):
        test = pymccrgb.core.classify_ground_mcc(self.data, scale, tol)
        true = np.load(
            os.path.join(TEST_OUTPUT_DIR, f"classification_mcc_{scale}_{tol}.npy"),
            allow_pickle=True,
        )
        self.assertSequenceEqual(
            test.tolist(),
            true.tolist(),
            f"MCC ground classification is incorrect for scale {scale} and height tolerance {tol}",
        )

    def test_mcc_classification(self):
        for scale in TEST_SCALES:
            for tol in TEST_TOLS:
                self._test_classify_ground_mcc(scale, tol)

    def test_mcc_default(self):
        test_points, test_labels = pymccrgb.core.mcc(self.data, verbose=True)
        true_points, true_labels = np.load(
            os.path.join(TEST_OUTPUT_DIR, f"ground_labels_mcc_default.npy"),
            allow_pickle=True,
        )
        self.assertTrue(
            np.allclose(test_points, true_points),
            "Ground points are incorrect for default MCC configuration",
        )
        self.assertSequenceEqual(
            test_labels.tolist(),
            true_labels.tolist(),
            "Classification is incorrect for default MCC configuration",
        )


class MCCRGBTestCase(unittest.TestCase):
    def setUp(self):
        self.data = pymccrgb.ioutils.read_las(
            os.path.join(TEST_DATA_DIR, "points_rgb.laz")
        )

    def test_mcc_rgb_default(self):
        test_points, test_labels = pymccrgb.core.mcc_rgb(
            self.data, seed=SEED_VALUE, verbose=True
        )
        true_points, true_labels = np.load(
            os.path.join(TEST_OUTPUT_DIR, f"ground_labels_mccrgb_default.npy"),
            allow_pickle=True,
        )
        self.assertTrue(
            np.allclose(test_points, true_points),
            "Ground points are incorrect for default MCC-RGB configuration",
        )
        self.assertSequenceEqual(
            test_labels.tolist(),
            true_labels.tolist(),
            "Classification is incorrect for default MCC-RGB configuration",
        )

    def test_mcc_rgb_two_training_tols(self):
        test_points, test_labels = pymccrgb.core.mcc_rgb(
            self.data,
            tols=[1.0, 0.3, 0.3],
            training_tols=[1.0, 0.3],
            training_scales=[0.5, 0.5],
            seed=SEED_VALUE,
            verbose=True,
        )
        true_points, true_labels = np.load(
            os.path.join(TEST_OUTPUT_DIR, f"ground_labels_mccrgb_twotols_1.0_0.3.npy"),
            allow_pickle=True,
        )
        self.assertTrue(
            np.allclose(test_points, true_points),
            "Ground points are incorrect for default MCC-RGB configuration",
        )
        self.assertSequenceEqual(
            test_labels.tolist(),
            true_labels.tolist(),
            "Classification is incorrect for default MCC-RGB configuration",
        )

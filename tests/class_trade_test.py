"""
Module with unit test for class Trade
"""
import unittest
import pandas as pd
import numpy as np
import settings
from class_trade import Trade


class TestTrade(unittest.TestCase):

    def test_scale_coordinates(self):
        test_data = Trade(file_path=settings.TESTS_PATH, separator=';')
        test_data.scale_coordinates(factor=-1)
        result_data = test_data.get_data()
        expected_x = pd.Series([-1.0, -2.0, -3.0, -4.0], name='x')
        expected_y = pd.Series([-1.0, -2.0, -3.0, -4.0], name='y')
        pd.testing.assert_series_equal(result_data['x'], expected_x)
        pd.testing.assert_series_equal(result_data['y'], expected_y)

    def test_convert_reference_frame(self):
        test_data = Trade(file_path=settings.TESTS_PATH, separator=';')
        test_data.convert_reference_frame(displacement_vector=(1.0, 1.0))
        result_data = test_data.get_data()
        expected_x = pd.Series([0.0, 1.0, 2.0, 3.0], name='x')
        expected_y = pd.Series([0.0, 1.0, 2.0, 3.0], name='y')
        pd.testing.assert_series_equal(result_data['x'], expected_x)
        pd.testing.assert_series_equal(result_data['y'], expected_y)

    def test_get_mean_velocity(self):
        test_data = Trade(file_path=settings.TESTS_PATH, separator=';')
        expected = pd.Series([np.nan, 1.41, 1.41, 1.41])
        resulted = test_data.get_mean_velocity()
        pd.testing.assert_series_equal(resulted, expected, atol=1e4)

    def test_get_com(self):
        test_data = Trade(file_path=settings.TESTS_PATH, separator=';')
        expected = (2.5, 2.5)
        resulted = test_data.get_com()
        self.assertTupleEqual(resulted, expected)

    def test_com_distance_list(self):
        pass





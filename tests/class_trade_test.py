"""
Module with unit test for class Trade
"""
import unittest
import pandas as pd
import settings
from class_trade import Trade


class TestTrade(unittest.TestCase):

    # def test_create_trade_object(self):
    #     expected = Trade()

    def test_scale_coordinates(self):
        expected_x = pd.Series([-1.0, -2.0], name='x')
        expected_y = pd.Series([-3.0, -4.0], name='y')
        result = Trade(file_path=settings.TESTS_PATH, separator=';')
        result.scale_coordinates(factor=-1)
        result_x = result.get_x()
        result_y = result.get_y()
        pd.testing.assert_series_equal(result_x, expected_x)
        pd.testing.assert_series_equal(result_y, expected_y)


    # def test_convert_reference_frame(self):
    #     expected_x = pd.Series([], name)


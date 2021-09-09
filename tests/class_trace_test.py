"""
Module with unit test for class Trade. Paths to test data can be changed in settings.py.
"""
import unittest

import numpy as np
import pandas as pd

from class_trace import Trace


class TestTrace(unittest.TestCase):

    TEST_DATA = './test_data.csv'
    TEST_PREDEFINED_POINTS = './test_predefined_points.csv'
    TEST_RESAMPLE_DATA = './test_resample_data_50hz.csv'
    EPSILON = 1e-5
    DECIMAL_NUMBER = 5

    def test_object_trace(self):
        """
        Function to test creating Trace object from file. Test checks that the expected and result dataframes are
        the same (indexes and data).
        """
        test_data = Trace(file_path=self.TEST_DATA, separator=';')
        result_data = test_data.get_data()
        expect_index = pd.DatetimeIndex(['2018-01-01 00:00:01.000', '2018-01-01 00:00:02.000',
                                         '2018-01-01 00:00:03.000', '2018-01-01 00:00:04.000'])
        expect_data = pd.DataFrame(index=expect_index, data={'x': [1.0, 2.0, 3.0, 4.0], 'y': [-1.0, -2.0, -3.0, -4.0],
                                                             'Unnamed: 3': [np.nan, np.nan, np.nan, np.nan]})
        pd.testing.assert_frame_equal(result_data, expect_data)

    def test_resample_data(self):
        """
        Function to test changing sampling frequency of input signal. Test check that the expected and result series
        x and y coordinates are the same with atol=self.EPSILON error.
        :return:
        """
        test_data = Trace(file_path=self.TEST_RESAMPLE_DATA, separator=',')
        test_data.resample_data(original_freq_hz=50, expected_freq_hz=20, interpolation_method='linear')
        result_data = test_data.get_data()
        expect_index = pd.DatetimeIndex(['2021-01-01 00:00:00.000', '2021-01-01 00:00:00.050',
                                         '2021-01-01 00:00:00.100', '2021-01-01 00:00:00.150',
                                         '2021-01-01 00:00:00.200', '2021-01-01 00:00:00.250'], freq='50L')
        expect_x = pd.Series([0.0, 2.5, 0.0, 2.5, 0.0, 2.5], name='x', index=expect_index)
        expect_y = pd.Series([0.0, -2.5, 0.0, -2.5, 0.0, -2.5], name='y', index=expect_index)
        pd.testing.assert_series_equal(result_data['x'], expect_x, atol=self.EPSILON)
        pd.testing.assert_series_equal(result_data['y'], expect_y, atol=self.EPSILON)

    def test_scale_coordinates(self):
        """
        Function to test scaling coordinates by multiplying factor. Test checks that the expected and result series
        x and y coordinates are the same with atol=self.EPSILON error.
        """
        expect_index = pd.DatetimeIndex(['2018-01-01 00:00:01.000', '2018-01-01 00:00:02.000',
                                         '2018-01-01 00:00:03.000', '2018-01-01 00:00:04.000'])
        test_factors = [0, -1, 1000000]
        expect_x_list = [[0.0, 0.0, 0.0, 0.0],
                         [-1.0, -2.0, -3.0, -4.0],
                         [1000000.0, 2000000.0, 3000000.0, 4000000.0]]
        expect_y_list = [[0.0, 0.0, 0.0, 0.0],
                         [1.0, 2.0, 3.0, 4.0],
                         [-1000000.0, -2000000.0, -3000000.0, -4000000.0]]
        for ind, i in enumerate(test_factors):
            test_data = Trace(file_path=self.TEST_DATA, separator=';')
            test_data.scale_coordinates(factor=i)
            result_data = test_data.get_data()
            expect_x = pd.Series(data=expect_x_list[ind], name='x', index=expect_index)
            expect_y = pd.Series(data=expect_y_list[ind], name='y', index=expect_index)
            pd.testing.assert_series_equal(result_data['x'], expect_x, atol=self.EPSILON)
            pd.testing.assert_series_equal(result_data['y'], expect_y, atol=self.EPSILON)

    def test_convert_reference_frame(self):
        """
        Function to test converting reference frame by displacement vector. Test checks that the expected and result
        series x and y coordinates are the same with atol=self.EPSILON error.
        """
        expect_index = pd.DatetimeIndex(['2018-01-01 00:00:01.000', '2018-01-01 00:00:02.000',
                                         '2018-01-01 00:00:03.000', '2018-01-01 00:00:04.000'])
        test_displacement_vector = [(0.0, 0.0), (1.0, -1.0), (10, -10)]
        expect_x_list = [[1.0, 2.0, 3.0, 4.0],
                         [0.0, 1.0, 2.0, 3.0],
                         [-9.0, -8.0, -7.0, -6.0]]
        expect_y_list = [[-1.0, -2.0, -3.0, -4.0],
                         [0.0, -1.0, -2.0, -3.0],
                         [9.0, 8.0, 7.0, 6.0]]
        for ind, i in enumerate(test_displacement_vector):
            test_data = Trace(file_path=self.TEST_DATA, separator=';')
            test_data.convert_reference_frame(displacement_vector=i)
            result_data = test_data.get_data()
            expect_x = pd.Series(data=expect_x_list[ind], name='x', index=expect_index)
            expect_y = pd.Series(data=expect_y_list[ind], name='y', index=expect_index)
            pd.testing.assert_series_equal(result_data['x'], expect_x, atol=self.EPSILON)
            pd.testing.assert_series_equal(result_data['y'], expect_y, atol=self.EPSILON)

    def test_get_mean_velocity(self):
        """
        Function to test calculating mean velocity from data. Test checks that the expected and result series with
        velocity values are the same with atol=self.EPSILON error.
        """
        test_data = Trace(file_path=self.TEST_DATA, separator=';')
        expect_index = pd.DatetimeIndex(['2018-01-01 00:00:01.000', '2018-01-01 00:00:02.000',
                                         '2018-01-01 00:00:03.000', '2018-01-01 00:00:04.000'])
        expect = pd.Series([np.nan, 1.41421, 1.41421, 1.41421], index=expect_index)
        result = test_data.get_mean_velocity()
        pd.testing.assert_series_equal(result, expect, atol=self.EPSILON)

    def test_get_com(self):
        """
        Function to test calculating center of mass(COM). Test checks that the expected and result Tuples with COM
        are the same with decimal=self.DECIMAL_NUMBER precision.
        """
        test_data = Trace(file_path=self.TEST_DATA, separator=';')
        expect = (2.5, -2.5)
        result = test_data.get_com()
        np.testing.assert_almost_equal(result, expect, decimal=self.DECIMAL_NUMBER)

    def test_com_distance_list(self):
        """
        Function to test calculating distances between test predefined points and COM. Test predefined points are loaded
        from file. Test checks that the expected and result List with distances are the same
        with decimal=self.DECIMAL_NUMBER precision.
        """
        test_data = Trace(file_path=self.TEST_DATA, separator=';')
        points = pd.read_csv(self.TEST_PREDEFINED_POINTS, sep=';')
        result = test_data.get_com_distance_list(points)
        expect = [3.80788, 4.52769, 5.52268, 6.67083]
        np.testing.assert_almost_equal(result, expect, decimal=self.DECIMAL_NUMBER)


if __name__ == '__main__':
    unittest.main()

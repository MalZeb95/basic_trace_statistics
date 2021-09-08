"""
Software prepared for initial signal processing and basic statistics generation useful for further analysis.
Module contains main core of initial analysis of trade and functions which uploads needed input data from .csv file.
Predefined points used in get_com_distance_list can be generated and saved to file -> class PredefinedPoints
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import settings


class Trade:
    """
    Class prepared to generate basic statistics of drawn trace. Based on coordinates (x,y), software allows to obtain:
    - processing of the signal into a necessary sampling rate,
    - conversion into different unit system and reference frame,
    - calculation of the mean velocity, center of mass(COM) and distance between COM and predefined points,
    - visualisation of the trace, center of mass and predefined points.
    """
    def __init__(self, file_path, separator='\t'):

        self.data = pd.read_csv(file_path, sep=separator, dtype={'Unnamed: 0': str, 'x': float, 'y': float})
        self.datetime_column = 'Unnamed: 0'  # Name of column with time and date string
        self.data[self.datetime_column] = pd.to_datetime(self.data[self.datetime_column], format='%Y-%m-%d %H:%M:%S.%f')

    def resample_data(self, expected_freq_hz=20):
        """
        Function convert signal sampled with origin_freq_hz frequency into expected_freq_hz
        :param data: data as DataFrame
        :param origin_freq_hz: int value of origin sampling frequency in Hz
        :param expected_freq_hz: int value of expected sampling frequency in Hz
        :return: data
        """
        # dorobić tą funkcję lepiej Bo nie działa!!!!!!!!!!!!!!!!!!!!!
        self.data[string_column].subtract(self.data[string_column][0]).dt.total_seconds()
        timedelta_test = timedelta(seconds=expected_freq_hz/1)

        test = self.data.resample(rule=timedelta_test)
        print('test resample')
        return test

    def scale_coordinates(self, factor=10.0):
        """
        Fuction which scales coordinates by multiplying x,y values with factor
        :param data: data in DataFrame
        :param factor: scalar for scaling coordinates
        :return: data
        """
        self.data['x'] = self.data['x']*factor
        self.data['y'] = self.data['y']*factor

    def convert_reference_frame(self, displacement_vector=(0.0, 0.0)):
        """
        Function convert reference frame into another used discplacement_vector
        :param displacement_vector:
        :return:
        """
        self.data['x'] = self.data['x'].subtract(displacement_vector[0])
        self.data['y'] = self.data['y'].subtract(displacement_vector[1])

    def get_mean_velocity(self):
        """
        Function calculate mean velocity of drawn trace based on (x,y) coordinates and datetime vector.
        First value is NaN due to the differences calculated between neighboring elements.
        :param data: DataFrame with coordinates and time
        :return: data
        """
        diff_data = self.data.diff()
        velocity_x = diff_data['x'] / diff_data[self.datetime_column].dt.total_seconds()
        velocity_y = diff_data['y'] / diff_data[self.datetime_column].dt.total_seconds()
        mean_velocity_temp = velocity_x.pow(2).add(velocity_y.pow(2))
        mean_velocity = mean_velocity_temp.pow(0.5)
        return mean_velocity

    def get_com(self):
        """
        Fuction calculate center of mass of signal as a list with two elements [x_com, y_com]
        :param data:
        :return:
        """
        x_com = self.data['x'].mean()
        y_com = self.data['y'].mean()
        return x_com, y_com

    def get_com_distance_list(self, predefined_points):
        """
        Function generate list of distances between predefined points (x,y) and center of mass from original .csv data
        :return: list
        """
        com_x, com_y = self.get_com()
        distances_x = predefined_points['x'].subtract(com_x).pow(2)
        distances_y = predefined_points['y'].subtract(com_y).pow(2)
        distances_temp = distances_x.add(distances_y)
        distances = distances_temp.pow(0.5).tolist()
        return distances

    def get_plot(self, filename, predefined_points=None):
        """
        Function to visualize trace, center of mass and predefined points
        :param data: DataFrame with x,y coordinates
        :param predefined_points: dataframe with predefined points
        :param filename: string with extension
        :return:
        """

        com_x, com_y = self.get_com()
        fig, ax = plt.subplots()
        ax.plot(self.data['x'], self.data['y'])
        ax.scatter(com_x, com_y, c='orange')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend(['data', 'COM'])
        if predefined_points is not None:
            ax.scatter(predefined_points['x'], predefined_points['y'], c='green')
            ax.legend(['data', 'COM', 'predefined'])
        plt.savefig(os.path.join(settings.REPORTS_PATH, filename))
        plt.show()

    def get_data(self):
        return self.data


def main():

    data = Trade(file_path=settings.DATA_PATH)
    data.scale_coordinates(factor=10.0)
    data.convert_reference_frame((5., 0))
    data.scale_coordinates(factor=.1)
    #test_resample = data.resample_data(expected_freq_hz=20)
    data.convert_reference_frame(displacement_vector=(10, 10))
    test_velocity = data.get_mean_velocity()
    test_com = data.get_com()
    points = pd.read_csv(settings.PREDEFINED_POINTS_PATH, sep=',')
    test_distance = data.get_com_distance_list(points)
    data.get_plot(filename='interview_task_plot.jpg', predefined_points=None)

    print('Trade statistics:')
    print(f' 1. CENTER OF MASS: {test_com},')
    print(f' 2. MEAN VELOCITY: {test_velocity},')
    print(f' 3. DISTANCES: {test_distance},')


if __name__ == '__main__':
    main()

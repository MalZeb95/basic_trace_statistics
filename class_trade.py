"""
Software prepared for initial signal processing and basic statistics generation useful for further analysis.
Module contains main core of initial analysis of trade and functions which uploads needed input data from .csv file.
Predefined points used in get_com_distance_list can be generated and saved to file -> class PredefinedPoints
"""
import os

import pandas as pd
import matplotlib.pyplot as plt
import settings
from class_predefined_points import PredefinedPoints


class Trade:
    """
    Class prepared to generate basic statistics of drawn trace. Based on coordinates (x,y), software allows to obtain:
    - processing of the signal into a necessary sampling rate,
    - conversion into different unit system and reference frame,
    - calculation of the mean velocity, center of mass(COM) and distance between COM and predefined points,
    - visualisation of the trace, center of mass and predefined points.
    """
    def __init__(self, file_path, separator='\t'):
        self.data = pd.read_csv(file_path, sep=separator)

    def convert_string_column_to_time(self, col_str_index=0):
        """
        Function convert first column with string (info about date and time sample) into time vector
        :param data: DataFrame with signals and string column(data and time)
        :param col_str_index: index of string column
        :return: data
        """
        column_names = self.data.columns
        string_column = column_names[col_str_index]
        self.data[string_column] = pd.to_datetime(self.data[string_column], format='%Y-%m-%d %H:%M:%S.%f')
        self.data[string_column] = self.data[string_column].dt.strftime('%S.%f')
        self.data[string_column] = self.data[string_column].astype(float)
        self.data = self.data.rename(columns={string_column: "time"})

    def resample_data(self, data, origin_freq_hz=50, expected_freq_hz=20):
        """
        Function convert signal sampled with origin_freq_hz frequency into expected_freq_hz
        :param data: data as DataFrame
        :param origin_freq_hz: int value of origin sampling frequency in Hz
        :param expected_freq_hz: int value of expected sampling frequency in Hz
        :return: data
        """
        # dorobić tą funkcję lepiej Bo nie działa!!!!!!!!!!!!!!!!!!!!!
        test = data.resample('50ms')
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

    def convert_reference_frame(self, displacement_vector=(0, 0)):
        """
        Function convert reference frame into another used discplacement_vector
        :param displacement_vector:
        :return:
        """
        self.data['x'] = self.data['x'].subtract(displacement_vector[0])
        self.data['x'] = self.data['x'].subtract(displacement_vector[1])

    def get_mean_velocity(self):
        """
        Function calculate mean velocity of drawn trace based on (x,y) coordinates and time vector
        :param data: DataFrame with coordinates and time
        :return: data
        """
        diff_data = self.data.diff()
        velocity_x = diff_data['x']/diff_data['time']
        velocity_y = diff_data['y'] / diff_data['time']
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
        Function generate list of distances between given (x,y) coordinates and center of mass from original .csv data
        :param predefined_points: DataFrame with two columns ['x' and 'y']
        :return: list
        """
        com_x, com_y = self.get_com()
        distances_x = predefined_points['x'].subtract(com_x).pow(2)
        distances_y = predefined_points['y'].subtract(com_y).pow(2)
        distances_temp = distances_x.add(distances_y)
        distances = distances_temp.pow(0.5).tolist()
        return distances

    def get_plot(self, predefined_points, filename):
        """
        Function to visualize trace, center of mass and predefined points
        :param data: DataFrame with x,y coordinates
        :param predefined_points: dataframe with predefined points
        :param filename: string with extension
        :return:
        """

        fig, ax = plt.subplots()
        ax.plot(self.data['x'], self.data['y'])
        ax.scatter(predefined_points['x'], predefined_points['y'])
        com_x, com_y = self.get_com()
        ax.scatter(com_x, com_y)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend(['data', 'predefined', 'com'])
        plt.savefig(os.path.join(settings.REPORTS_PATH, filename))
        plt.show()


def main():

    data_object = Trade(file_path=settings.DATA_PATH)
    data_object.convert_string_column_to_time(col_str_index=0)
    data_object.scale_coordinates(factor=10.0)
    data_object.convert_reference_frame(displacement_vector=(10, 10))
    test_velocity = data_object.get_mean_velocity()
    test_com = data_object.get_com()
    pred_object = PredefinedPoints(filename='predefined_points.csv', points_number=100)
    additional_data = pred_object.get_signal_from_file()
    test_distance = data_object.get_com_distance_list(additional_data)
    data_object.get_plot(additional_data, filename='interview_task_plot.jpg')

    print('Test running... data loaded from csv')


if __name__ == '__main__':
    main()

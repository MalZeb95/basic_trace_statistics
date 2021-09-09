"""
Software prepared for initial signal processing and basic statistics generation. Local paths to files could be changed
in settings.py.
"""
import os

import math
import matplotlib.pyplot as plt
import pandas as pd
from typing import Union

import settings


class Trace:
    """
    Class prepared to generate basic statistics of drawn trace. Based on coordinates (x,y) from input .csv data,
    functions allow to obtain:
    - processing of the signal into a necessary sampling rate,
    - conversion into different unit systems and reference frame,
    - calculation of the mean velocity, center of mass(COM) and distance between COM and predefined points,
    - visualisation of the trace, center of mass and predefined points.
    """

    def __init__(self, file_path, separator='\t', index_column=0):
        self.data = pd.read_csv(file_path, sep=separator, dtype={'x': float, 'y': float}, index_col=index_column)
        self.data.index = pd.to_datetime(self.data.index, format='%Y-%m-%d %H:%M:%S.%f')

    def resample_data(self, original_freq_hz=50, expected_freq_hz=20, interpolation_method='linear'):
        """
        Function converts loaded DataFrame into data sampled with expected_freq_hz frequency.
        :param original_freq_hz: int value of original sampling frequency in Hz
        :param expected_freq_hz: int value of expected sampling frequency in Hz
        :param interpolation_method: string with name of interpolation method
        """
        least_common_multiple = abs(original_freq_hz * expected_freq_hz) // math.gcd(original_freq_hz, expected_freq_hz)
        rule_for_resampling = pd.Timedelta(1 / least_common_multiple, unit='s')
        self.data = self.data.resample(rule=rule_for_resampling).interpolate(method=interpolation_method)
        rule_for_resampling_2 = pd.Timedelta(1 / expected_freq_hz, unit="s")
        self.data = self.data.resample(rule=rule_for_resampling_2).interpolate(method=interpolation_method)

    def scale_coordinates(self, factor=1.0):
        """
        Function scales coordinates in DataFrame by multiplying x,y values by the factor.
        :param factor: float scalar for scaling coordinates
        """
        self.data['x'] *= factor
        self.data['y'] *= factor

    def convert_reference_frame(self, displacement_vector=(0.0, 0.0)):
        """
        Function converts reference frame into another used displacement_vector.
        :param displacement_vector: Tuple with two float step values for x(left) and y(right) axis
        """
        self.data['x'] = self.data['x'].subtract(displacement_vector[0])
        self.data['y'] = self.data['y'].subtract(displacement_vector[1])

    def get_mean_velocity(self):
        """
        Function calculates mean velocity of drawn trace based on (x,y) coordinates and datetime vector.
        First value is NaN due to the differences calculated between neighboring elements.
        :return: Series with mean velocity values
        """
        diff_data = self.data.diff()
        time_diff = self.data.index.to_series().diff()
        velocity_x = diff_data['x'] / time_diff.dt.total_seconds()
        velocity_y = diff_data['y'] / time_diff.dt.total_seconds()
        mean_velocity_temp = velocity_x.pow(2).add(velocity_y.pow(2))
        mean_velocity = mean_velocity_temp.pow(0.5)
        return mean_velocity

    def get_com(self):
        """
        Function calculates center of mass(COM) of signals x and y.
        :return coordinates of COM
        """
        x_com = self.data['x'].mean()
        y_com = self.data['y'].mean()
        return x_com, y_com

    def get_com_distance_list(self, predefined_points: pd.DataFrame):
        """
        Function calculates distances between DataFrame predefined points (x,y) and COM from original .csv input data.
        :param predefined_points: DataFrame with points (x,y); predefined points need to be loaded from external file.
        :return: list with distances values
        """
        com_x, com_y = self.get_com()
        distances_x = predefined_points['x'].subtract(com_x).pow(2)
        distances_y = predefined_points['y'].subtract(com_y).pow(2)
        distances_temp = distances_x.add(distances_y)
        distances = distances_temp.pow(0.5).tolist()
        return distances

    def draw_plot(self, filename: str, predefined_points: Union[None, pd.DataFrame]):
        """
        Function visualizes trace, center of mass and predefined points and saves result to file. It is possible to
        generate plot without predefined points.
        :param filename: name of figure with extension. File will be saved in REPORTS_PATH set in settings.py,
        :param predefined_points: DataFrame with predefined points
        """
        com_x, com_y = self.get_com()
        fig, ax = plt.subplots()
        ax.plot(self.data['x'], self.data['y'])
        ax.scatter(com_x, com_y, c='orange')
        legend = ['data', 'COM']
        if predefined_points is not None:
            ax.scatter(predefined_points['x'], predefined_points['y'], c='green')
            legend.append('predefined')
        ax.legend(legend)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.show()
        file_path = os.path.join(settings.REPORTS_PATH, filename)
        if os.path.isfile(file_path):
            print(f'{filename} is already exist. Select different name for file to save plot.')
        else:
            plt.savefig(file_path)

    def get_data(self):
        return self.data


def main():
    data = Trace(file_path=settings.DATA_PATH)
    data.resample_data(original_freq_hz=50, expected_freq_hz=20, interpolation_method='linear')
    data.scale_coordinates(factor=10.)
    data.convert_reference_frame((5., 0))
    com = data.get_com()
    mean_velocity = data.get_mean_velocity()
    points = pd.read_csv(settings.PREDEFINED_POINTS_PATH, sep=',')
    distances = data.get_com_distance_list(points)
    data.draw_plot(filename='new_plot.jpg', predefined_points=points)

    print('Trace statistics:')
    print(f' 1. CENTER OF MASS: {com},')
    print(f' 2. MEAN VELOCITY: {mean_velocity},')
    print(f' 3. DISTANCES: {distances},')


if __name__ == '__main__':
    main()

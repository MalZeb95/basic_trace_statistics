"""
Software prepared for initial signal processing and basic statistics generation. Local paths to files could be changed
in settings.py.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import settings


class Trade:
    """
    Class prepared to generate basic statistics of drawn trace. Based on coordinates (x,y) from input .csv data,
    functions allow to obtain:
    - processing of the signal into a necessary sampling rate,
    - conversion into different unit systems and reference frame,
    - calculation of the mean velocity, center of mass(COM) and distance between COM and predefined points,
    - visualisation of the trace, center of mass and predefined points.
    """
    def __init__(self, file_path, separator='\t'):

        self.data = pd.read_csv(file_path, sep=separator, dtype={'Unnamed: 0': str, 'x': float, 'y': float})
        self.datetime_column = 'Unnamed: 0'  # Name of column with time and date string
        self.data[self.datetime_column] = pd.to_datetime(self.data[self.datetime_column], format='%Y-%m-%d %H:%M:%S.%f')

    def resample_data(self, expected_freq_hz=20):
        """
        Function converts loaded DataFrame into data sampled with expected_freq_hz frequency.
        :param expected_freq_hz: int value of expected sampling frequency in Hz
        """
        self.data[self.datetime_column].subtract(self.data[self.datetime_column][0])  # To obtain timedelta column
        rule_for_resampling = pd.Timedelta(1/expected_freq_hz, unit="s")
        test = self.data.resample(rule=rule_for_resampling, on=self.datetime_column)
        return test

    def scale_coordinates(self, factor=10.0):
        """
        Function scales coordinates in DataFrame by multiplying x,y values by the factor.
        :param factor: scalar for scaling coordinates
        """
        self.data['x'] = self.data['x']*factor
        self.data['y'] = self.data['y']*factor

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
        velocity_x = diff_data['x'] / diff_data[self.datetime_column].dt.total_seconds()
        velocity_y = diff_data['y'] / diff_data[self.datetime_column].dt.total_seconds()
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

    def get_com_distance_list(self, predefined_points):
        """
        Function calculates distances between DataFrame predefined points (x,y) and COM from original .csv input data.
        :predefined points: DataFrame with points (x,y); predefined points need to be loaded from external file.
        :return: list with distances values
        """
        com_x, com_y = self.get_com()
        distances_x = predefined_points['x'].subtract(com_x).pow(2)
        distances_y = predefined_points['y'].subtract(com_y).pow(2)
        distances_temp = distances_x.add(distances_y)
        distances = distances_temp.pow(0.5).tolist()
        return distances

    def get_plot(self, filename, predefined_points=None):
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
    # test_resample = data.resample_data(expected_freq_hz=20)
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

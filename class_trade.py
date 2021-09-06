"""
Software prepared for initial signal processing and basic statistics generation useful for further analysis.
Module contains main core of initial analysis of trade and functions which uploads needed input data from .csv file.
Predefined points used in get_com_distance_list can be generated and saved to file -> class PredefinedPoints
"""

import pandas as pd
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
        self.data = pd.read_csv(file_path, sep=separator)

    def get_timestamp_from_string(self, data, col_str_index=0):
        """
        Function convert first column with string (info about date and time sample) into time vector
        :param data: DataFrame with signals and string column(data and time)
        :param col_str_index: index of string column
        :return: data
        """
        column_names = data.columns
        string_column = column_names[col_str_index]
        data[string_column] = pd.to_datetime(data[string_column], format='%Y-%m-%d %H:%M:%S.%f')
        data[string_column] = data[string_column].dt.strftime('%S.%f')
        data = data.rename(columns={string_column: "time"})
        return data


def main():

    file = settings.DATA_PATH
    data_object = Trade(file_path=file)
    dane = data_object.data
    converted = data_object.get_timestamp_from_string(data=dane, col_str_index=0)
    print('Test running... data loaded from csv')


if __name__ == '__main__':
    main()

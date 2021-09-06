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
    def __init__(self, file_path, separator='\t', index_column=0):
        self.data = pd.read_csv(file_path, sep=separator, index_col=index_column)


def main():

    file = settings.DATA_PATH
    data_object = Trade(file_path=file)
    dane = data_object.data
    print('Test running... data loaded from csv')


if __name__ == '__main__':
    main()

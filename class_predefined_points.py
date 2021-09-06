"""
Module prepared to generate additional data- predefined points, used to analysis.
"""
import os
import settings
import numpy as np
import pandas as pd


class PredefinedPoints:
    def __init__(self, filename, points_number):
        self.filename = filename
        self.points_number = points_number
        self.file_path = os.path.join(settings.REPORTS_PATH, self.filename)
        t = np.linspace(0, 2 * np.pi, self.points_number)
        r = 6 + np.cos(t)
        x, y = r * np.cos(t), r * np.sin(t)
        self.signal = pd.DataFrame({'x': x, 'y': y})
        self.signal.to_csv(self.file_path)

    def get_signal_from_file(self):
        signal = pd.read_csv(self.file_path)
        return signal

import random
from dataclasses import dataclass

from lanka_data_timeseries import constants
from lanka_data_timeseries.cbsl.Frequency import Frequency
from lanka_data_timeseries.cbsl.FREQUENCY_LIST import FREQUENCY_LIST


@dataclass
class Config:
    frequency: Frequency
    i_subject: int

    def __str__(self):
        return f'Config({self.frequency.name}, {self.i_subject})'

    def __repr__(self):
        return str(self)

    @staticmethod
    def random_list() -> list:
        config_list = []
        for frequency in FREQUENCY_LIST:
            for i_subject in range(0, constants.N_SUBJECTS):
                config_list.append(Config(frequency, i_subject))

        random.shuffle(config_list)
        return config_list

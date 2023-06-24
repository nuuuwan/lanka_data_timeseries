from dataclasses import dataclass

from utils import Time, TimeFormat


def get_next_year():
    return int(TimeFormat('%Y').stringify(Time.now())) + 1


@dataclass
class Frequency:
    name: str
    value: str
    from_str: str
    to_str: str

    def __str__(self):
        return f'Frequency({self.name})'

    def __repr__(self):
        return str(self)


END_YEAR = get_next_year()
START_YEAR = END_YEAR - 40

FREQUENCY_LIST = [
    Frequency('Annual', 'A', START_YEAR, END_YEAR),
    # Frequency('Monthly', 'M', f'{START_YEAR}-01', f'{END_YEAR}-01'),
    # Frequency('Census Year', 'C', START_YEAR, END_YEAR),
    # Frequency('Academic Year', 'E', START_YEAR,END_YEAR),
    # Frequency('Daily', 'D', f'{START_YEAR}-01-01', f'{END_YEAR}-01-01'),
    # Frequency('Half Yearly', 'H', '1970', '2024'),
    # Frequency('Quarterly', 'Q', '1970', '2024'),
    # Frequency('On-Availablity', 'O', '1970', '2024'),
]

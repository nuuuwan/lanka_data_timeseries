from dataclasses import dataclass


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


START_YEAR = str(1970)
END_YEAR = str(2024)

FREQUENCY_LIST = [
    Frequency('Annual', 'A', START_YEAR,END_YEAR),
    # Frequency('Census Year', 'C', START_YEAR, END_YEAR),
    # Frequency('Academic Year', 'E', START_YEAR,END_YEAR),
    # Frequency('Monthly', 'M', f'{START_YEAR}-01', f'{END_YEAR}-01'),
    # Frequency('Daily', 'D', f'{START_YEAR}-01-01', f'{END_YEAR}-01-01'),
    # Frequency('Half Yearly', 'H', '1970', '2024'),
    # Frequency('Quarterly', 'Q', '1970', '2024'),
    # Frequency('On-Availablity', 'O', '1970', '2024'),
]

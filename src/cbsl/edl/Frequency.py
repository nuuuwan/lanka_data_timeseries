from dataclasses import dataclass


@dataclass
class Frequency:
    name: str
    value: str
    from_str: str
    to_str: str


FREQUENCY_LIST = [Frequency('Annual', 'A', '1990', '2023')]

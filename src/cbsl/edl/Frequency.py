from dataclasses import dataclass


@dataclass
class FrequencyBase:
    name: str
    value: str
    from_str: str
    to_str: str


class Frequency:
    ANNUAL = FrequencyBase('Annual', 'A', '1970', '2023')

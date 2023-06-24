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


FREQUENCY_LIST = [Frequency('Annual', 'A', '1990', '2023')]

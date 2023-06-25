from dataclasses import dataclass


@dataclass
class Frequency:
    name: str
    value: str
    input_text_map: dict[str, str]

    def __str__(self):
        return f'Frequency({self.name})'

    def __repr__(self):
        return str(self)

from dataclasses import dataclass


@dataclass
class Size2D:
    width: int
    height: int

    def to_tuple(self):
        return (self.width, self.height)

    def __str__(self):
        return f'Size2D({self.width} x {self.height})'

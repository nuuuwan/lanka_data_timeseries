from dataclasses import dataclass


@dataclass
class Size2D:
    width: int
    height: int

    def to_tuple(self):
        return (self.width, self.height)

    def __str__(self):
        return f'Size2D({self.width} x {self.height})'


class Size2D16x9(Size2D):
    def __init__(self, width):
        super().__init__(width, int(width * 9 / 16))

from dataclasses import dataclass

from utils_future.Size2D import Size2D


@dataclass
class Point2D:
    x: int
    y: int

    def to_tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return f'Point2D({self.x}, {self.y})'

    def __add__(self, other):
        assert isinstance(other, Size2D)
        return Point2D(self.x + other.width, self.y + other.height)

from enum import Enum
from pyray import *

class Shape:
    side_count: int

    def render(self, x: int, y: int) -> None:
        draw_poly(Vector2(x, y), self.side_count, )
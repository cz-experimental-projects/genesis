from __future__ import annotations

from abc import ABC
from pyray import *


# Shape is a class that represents the visual appearance of an organ. It has a number of sides, a radius,
# a rotation, and a color. It can be rendered at a given x-y coordinate in the world.
class Shape(ABC):
    # The rotation of the shape, in degrees
    rotation: float
    # The color of the shape
    color: Color

    def __init__(self, rotation: float = 0, color: Color = WHITE) -> None:
        self.rotation = rotation
        self.color = color

    # Render the shape at the given x-y coordinate
    def render(self, x: int, y: int) -> None:
        pass

    # Create an empty shape with rotation 0, and white color
    @staticmethod
    def empty() -> Shape:
        return Shape(0, WHITE)


class PolygonShape(Shape):
    side_count: int
    radius: float

    def __init__(self, side_count: int, radius: float, rotation: float = 0, color: Color = WHITE) -> None:
        super().__init__(rotation, color)
        self.side_count = side_count
        self.radius = radius

    def render(self, x: int, y: int) -> None:
        draw_poly(Vector2(x, y), self.side_count, self.radius, self.rotation, self.color)


class RectangleShape(Shape):
    width: int
    height: int
    origin: Vector2

    def __init__(self, width: int, height: int, origin: Vector2 = Vector2(0.5, 0.5), rotation: float = 0, color: Color = WHITE) -> None:
        super().__init__(rotation, color)
        self.width = width
        self.height = height
        self.origin = origin

    def render(self, x: int, y: int) -> None:
        draw_rectangle_pro(Rectangle(x, y, self.width, self.height), self.origin, self.rotation, self.color)


class CircleShape(Shape):
    radius: float

    def __init__(self, radius: float, rotation: float = 0, color: Color = WHITE) -> None:
        super().__init__(rotation, color)
        self.radius = radius

    def render(self, x: int, y: int) -> None:
        draw_circle(x, y, self.radius, self.color)

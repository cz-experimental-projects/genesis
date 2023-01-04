from __future__ import annotations

from math import cos, sin, radians
from abc import ABC
from pyray import *

from genesis.utils.colors import COLOR_WHITE
from genesis.utils.utilities import from_angle_magnitude


# Shape is a class that represents the visual appearance of an organ. It has a number of sides, a radius,
# a rotation, and a color. It can be rendered at a given x-y coordinate in the world.
class Shape(ABC):
    # The rotation of the shape, in degrees
    rotation: float
    # The color of the shape
    color: Color

    def __init__(self, rotation: float = 0, color: Color = COLOR_WHITE) -> None:
        self.rotation = rotation
        self.color = color

    # Render the shape at the given x-y coordinate
    def render(self, x: int, y: int) -> None:
        pass

    # Get width of the shape
    def get_width(self) -> float:
        pass

    # Get height of the shape
    def get_height(self) -> float:
        pass

    # Apply x offset of the shape
    def apply_x_offset(self, x) -> float:
        pass

    # Apply y offset of the shape
    def apply_y_offset(self, y) -> float:
        pass

    # Get the local space for a position on the edge of given index
    def get_edge(self, angle: float) -> Vector2:
        pass

    # Create an empty shape with rotation 0, and white color
    @staticmethod
    def empty() -> Shape:
        return Shape(0, COLOR_WHITE)


class PolygonShape(Shape):
    side_count: int
    radius: float

    def __init__(self, side_count: int, radius: float, rotation: float = 0, color: Color = COLOR_WHITE) -> None:
        super().__init__(rotation, color)
        self.side_count = side_count
        self.radius = radius

    def render(self, x: int, y: int) -> None:
        draw_poly(Vector2(x, y), self.side_count, self.radius, self.rotation, self.color)

    def get_width(self) -> float:
        return self.radius * 2

    def get_height(self) -> float:
        return self.radius * 2

    def apply_x_offset(self, x) -> float:
        return x - self.radius

    def apply_y_offset(self, y) -> float:
        return y - self.radius

    def get_edge(self, angle: float) -> Vector2:
        return from_angle_magnitude(angle, self.radius)


class RectangleShape(Shape):
    width: int
    height: int
    origin: Vector2

    def __init__(self, width: int, height: int, origin: Vector2 = None, rotation: float = 0, color: Color = COLOR_WHITE) -> None:
        super().__init__(rotation, color)
        self.width = width
        self.height = height
        self.origin = Vector2(width * 0.5, height * 0.5) if origin is None else origin

    def render(self, x: int, y: int) -> None:
        draw_rectangle_pro(Rectangle(x, y, self.width, self.height), self.origin, self.rotation, self.color)

    def get_width(self) -> float:
        return self.width

    def get_height(self) -> float:
        return self.height

    def apply_x_offset(self, x) -> float:
        return x - self.origin.x

    def apply_y_offset(self, y) -> float:
        return y - self.origin.x

    def get_edge(self, angle: float) -> Vector2:
        # Convert the angle to radians
        angle_radians = radians(angle)
        # Calculate the x and y coordinates of the point on the circumference
        x = self.origin.x + (self.width / 2) * cos(angle_radians)
        y = self.origin.y + (self.height / 2) * sin(angle_radians)
        return Vector2(x, y)


class CircleShape(Shape):
    radius: float

    def __init__(self, radius: float, rotation: float = 0, color: Color = COLOR_WHITE) -> None:
        super().__init__(rotation, color)
        self.radius = radius

    def render(self, x: int, y: int) -> None:
        draw_circle(x, y, self.radius, self.color)

    def get_width(self) -> float:
        return self.radius * 2

    def get_height(self) -> float:
        return self.radius * 2

    def apply_x_offset(self, x) -> float:
        return x - self.radius

    def apply_y_offset(self, y) -> float:
        return y - self.radius

    def get_edge(self, angle: float) -> Vector2:
        return from_angle_magnitude(angle, self.radius)

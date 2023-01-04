import random

from pyray import Color, Vector2
from math import cos, sin, radians


def from_angle_magnitude(angle: float, magnitude: float) -> Vector2:
    angle_radians = radians(angle)
    x = cos(angle_radians) * magnitude
    y = sin(angle_radians) * magnitude
    return Vector2(x, y)


def check_chance(chance: float) -> bool:
    if not 0 <= chance <= 1:
        raise ValueError("Chance must be between 0 and 1, inclusive")

    # Convert the chance to a percentage
    percentage_chance = int(chance * 100)

    # Generate a random number between 1 and 100 and check if it is less than or equal to the percentage chance
    return random.randint(1, 100) <= percentage_chance


def darken_color(color: Color) -> Color:
    return Color(int(color.r * 0.9), int(color.g * 0.9), int(color.b * 0.9), color.a)


def lighten_color(color: Color) -> Color:
    return Color(int(color.r / 0.9), int(color.g / 0.9), int(color.b / 0.9), color.a)

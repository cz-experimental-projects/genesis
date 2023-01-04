from typing import Callable
from pyray import get_frame_time, Color

from genesis.organisms.organ import Gene, Organ
from genesis.utils.shape import Shape


# MaturityGene is a Gene that tracks the maturity of an Organ
class MaturityGene(Gene):
    # The maximum maturity level that this Organ can reach
    max_maturity: int
    # The current maturity level of this Organ
    current_maturity: float
    # Speed modifier of how fast this Organ will mature
    maturity_rate: float
    # Whether this Organ has reached its maximum maturity
    reached_max_maturity: bool
    # A callback function that is called when the Organ reaches its maximum maturity
    on_mature: Callable[[Organ], None]

    def __init__(self, max_maturity: int, on_mature: Callable[[Organ], None], organ: Organ, maturity_rate: float = 1):
        # Initialize the Gene with the organ and dominant attributes
        super().__init__(organ, True)
        # Initialize the max_maturity, current_maturity, and on_mature attributes
        self.max_maturity = max_maturity
        self.current_maturity = 0
        self.maturity_rate = maturity_rate
        self.reached_max_maturity = False
        self.on_mature = on_mature

    # Update the current_maturity attribute every frame
    def update(self) -> None:
        self.current_maturity += get_frame_time() * self.maturity_rate

        # If the current_maturity has reached the max_maturity, set reached_max_maturity to True and call the
        # on_mature callback
        if self.current_maturity >= self.max_maturity:
            self.reached_max_maturity = True
            self.on_mature(self.organ)


# ColorGene is a Gene that sets the color of an Organ's Shape
class ColorGene(Gene):
    # The color that this Gene sets for the Organ's Shape
    color: Color

    def __init__(self, color: Color, organ: Organ):
        # Initialize the Gene with the organ and dominant attributes
        super().__init__(organ, True)
        # Initialize the color attribute
        self.color = color

    # Set the color of the Organ's Shape when the Gene is initialized
    def initialize(self) -> None:
        self.organ.shape.color = self.color


# ShapeGene is a Gene that sets the Shape of an Organ
class ShapeGene(Gene):
    # The Shape that this Gene sets for the Organ
    shape: Shape

    def __init__(self, shape: Shape, organ: Organ):
        # Initialize the Gene with the organ and dominant attributes
        super().__init__(organ, False)
        # Initialize the shape attribute
        self.shape = shape

    # Set the Shape of the Organ when the Gene is initialized
    def initialize(self) -> None:
        self.organ.shape = self.shape


# HungerGene restricts the organ with energy
class EnergyGene(Gene):
    max_energy_level: int
    energy_level: float
    energy_depletion_rate: float

    def __init__(self, max_energy_level: int, organ: Organ, energy_depletion_rate: float = 1):
        super().__init__(organ, True)
        self.max_energy_level = max_energy_level
        self.energy_level = max_energy_level
        self.energy_depletion_rate = energy_depletion_rate

    def update(self) -> None:
        if self.energy_level <= 0:
            return

        self.energy_level -= get_frame_time() * self.energy_depletion_rate

    def replenish(self) -> None:
        self.energy_level = self.max_energy_level
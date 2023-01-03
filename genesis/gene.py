from abc import ABC
from typing import Callable

from genesis.organ import Organ


class Gene(ABC):
    organ: Organ

    def __init__(self, organ: Organ):
        self.organ = organ

    def initialize(self) -> None:
        pass

    def update(self) -> None:
        pass


class MaturityGene(Gene):
    max_maturity: int
    current_maturity: int
    reached_max_maturity: bool
    on_mature: Callable[[Organ], None]

    def __init__(self, max_maturity: int, organ: Organ, on_mature: Callable[[Organ], None]):
        super().__init__(organ)
        self.max_maturity = max_maturity
        self.current_maturity = 0
        self.reached_max_maturity = False

    def update(self) -> None:
        self.current_maturity += 1
        if self.current_maturity >= self.max_maturity:
            self.reached_max_maturity = True
            self.on_mature(self.organ)

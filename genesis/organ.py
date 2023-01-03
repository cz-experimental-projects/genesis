from __future__ import annotations
from genesis.gene import Gene


class Organ:
    to_remove: bool
    initialized: bool
    dna: list[Gene]
    organs: list[Organ]

    def __init__(self, dna: list[Gene]):
        self.to_remove = False
        self.initialized = False
        self.dna = dna
        self.organs = []

    def update(self) -> None:
        if not self.initialized:
            for gene in self.dna:
                gene.initialize()

            self.initialized = True

        for organ in self.organs:
            organ.update()

        for gene in self.dna:
            gene.update()

    def draw(self) -> None:
        for organ in self.organs:
            organ.draw()

    def remove(self) -> None:
        self.to_remove = True

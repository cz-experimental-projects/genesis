from __future__ import annotations

from abc import ABC
from typing import Optional, Callable
from events import Events
from pyray import is_mouse_button_released

from genesis.utils.shape import Shape
from genesis.utils.utilities import darken_color, lighten_color


# Gene is an abstract class that represents a genetic trait in an Organ
class Gene(ABC):
    # The Organ that this Gene belongs to
    organ: Organ
    # Whether this Gene is dominant or recessive
    dominant: bool

    def __init__(self, organ: Organ, dominant: bool):
        # Initialize the organ and dominant attributes
        self.organ = organ
        self.dominant = dominant

    # This method is called when the Gene is first added to the Organ
    def initialize(self) -> None:
        pass

    # This method is called every frame
    def update(self) -> None:
        pass

    def draw_gene_details(self, y_level: int) -> None:
        pass


# Organ is a class that represents a functional unit in an organism. It has DNA and child organs,
# and it can update itself, draw itself, and remove itself.
class Organ:
    # A flag indicating whether this organ should be removed
    to_remove: bool
    # A flag indicating whether this organ has been initialized
    initialized: bool
    # A flag to indicate if darken color change has been made
    darkened: bool
    # A flag to indicate if lighten color change has been made
    lightened: bool

    # The list of genes that belong to this organ
    dna: list[Gene]
    # The list of dominant genes that belong to this organ
    dominant_dna: list[Gene]

    # The list of child organs belonging to this organ
    children_organs: list[Organ]
    # The parent organ of this organ, if it has one
    parent_organ: Optional[Organ]

    # The shape of this organ
    shape: Shape

    # The x-coordinate of this organ in the world
    world_x: int
    # The y-coordinate of this organ in the world
    world_y: int
    # The x-coordinate of this organ in the local space relative to its parent
    local_x: int
    # The y-coordinate of this organ in the local space relative to its parent
    local_y: int

    # Things this organism wants to do but only if there is organs to receive it will it have an effect
    urges: Events

    def __init__(self, dna: list[Callable[[Organ], Gene]]):
        self.to_remove = False
        self.initialized = False
        self.darkened = False
        self.lightened = True

        self.dna = []
        self.dominant_dna = []

        self.children_organs = []
        self.parent_organ = None

        self.shape = Shape.empty()
        self.world_x = 0
        self.world_y = 0

        self.urges = Events((
            "on_walk",
            "on_ingest",
            "on_digest"
        ))

        # Create the genes specified in the dna list and add them to the appropriate list
        for gene_constructor in dna:
            created_gene = gene_constructor(self)
            if created_gene.dominant:
                self.dominant_dna.append(created_gene)
            else:
                self.dna.append(created_gene)

    # Update this organ and all of its children
    def update(self) -> None:
        if not self.initialized:
            # Initialize the genes
            for gene in self.dna:
                gene.initialize()

            for gene in self.dominant_dna:
                gene.initialize()

            self.initialized = True

        # Update the genes
        for gene in self.dna:
            gene.update()

        for gene in self.dominant_dna:
            gene.update()

        # Update the child organs
        for organ in self.children_organs:
            organ.update()

    # Draw this organ and all of its children
    def draw(self, organ_detail_ui) -> None:
        # If genes have not been initialized we do not draw
        if not self.initialized:
            return

        # Draw this organ if it has a shape
        if self.shape is not None:
            self.shape.render(int(self.world_x), int(self.world_y))

        # Draw the child organs
        for organ in self.children_organs:
            organ.draw(organ_detail_ui)

        from genesis.input import is_mouse_over_world_space

        # If mouse is hovering over, display options
        if is_mouse_over_world_space(self.shape.apply_x_offset(self.world_x), self.shape.apply_y_offset(self.world_y), self.shape.get_width(), self.shape.get_height()):
            if is_mouse_button_released(0):
                if organ_detail_ui.organ is not self:
                    organ_detail_ui.organ = self
            if not self.darkened:
                self.shape.color = darken_color(self.shape.color)
                self.darkened = True
                self.lightened = False
        elif not self.lightened:
            self.shape.color = lighten_color(self.shape.color)
            self.lightened = True
            self.darkened = False

    # Draw custom organ details if there is any
    def draw_organ_details(self, y_level: int):
        # If genes have not been initialized we do not draw
        if not self.initialized:
            return

        for gene in self.dominant_dna:
            gene.draw_gene_details(y_level)

        for gene in self.dna:
            gene.draw_gene_details(y_level)

    # Mark this organ for removal and remove it from its parent's children list
    def remove(self) -> None:
        self.to_remove = True
        if self.parent_organ is not None:
            self.parent_organ.children_organs.remove(self)
        if len(self.children_organs):
            for child in self.children_organs:
                child.remove()

    # Add a child organ to this organ
    def add_child_organ(self, organ: Organ) -> None:
        self.children_organs.append(organ)
        organ.parent_organ = self

    def move_pos_world_space(self, x: int, y: int) -> None:
        self.world_x = x
        self.world_y = y

        if self.parent_organ is not None:
            self.local_x = self.world_x - self.parent_organ.world_x
            self.local_y = self.world_y - self.parent_organ.world_y
        else:
            self.local_x = 0
            self.local_y = 0

        for child in self.children_organs:
            child.world_x = self.world_x + child.local_x
            child.world_y = self.world_y + child.local_y

    def move_pos_local_space(self, x: int, y: int) -> None:
        self.local_x = x
        self.local_y = y

        if self.parent_organ is not None:
            self.world_x = self.local_x + self.parent_organ.world_x
            self.world_y = self.local_y + self.parent_organ.world_y
        else:
            self.world_x = self.local_x
            self.world_y = self.local_y
            self.local_x = 0
            self.local_y = 0

        for child in self.children_organs:
            child.world_x = self.world_x + child.local_x
            child.world_y = self.world_y + child.local_y
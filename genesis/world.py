from pyray import Vector2
from genesis.organisms.organ import Organ


# World is a class that represents the environment in which organisms live. It contains a list of organisms
# and has methods for updating, drawing, and spawning organisms.
class World:
    # The list of organisms in the world
    organisms: list[Organ]
    # The list of organisms that are waiting to be added to the world
    organisms_add_queue: list[Organ]

    def __init__(self):
        self.organisms = []
        self.organisms_add_queue = []

    # Update all the organisms in the world
    def update(self) -> None:
        for organism in self.organisms:
            organism.update()

        # Remove marked organisms and add queued organisms
        self.__remove_marked_organisms()
        self.__add_queued_organisms()

    # Remove all organisms that have been marked for removal
    def __remove_marked_organisms(self) -> None:
        self.organisms = [organism for organism in self.organisms if not organism.to_remove]

    # Add all organisms that are in the add queue
    def __add_queued_organisms(self) -> None:
        for organism in self.organisms_add_queue:
            self.organisms.append(organism)
        self.organisms_add_queue.clear()

    # Draw all the organisms in the world
    def draw(self, organ_detail_ui) -> None:
        for organism in self.organisms:
            organism.draw(organ_detail_ui)

    # Spawn an organism at the given position in the world
    def spawn_with_vec2(self, organ: Organ, position: Vector2):
        self.spawn(organ, position.x, position.y)

    # Spawn an organism at the given x-y coordinate in the world
    def spawn(self, organ: Organ, world_x: int, world_y: int) -> None:
        organ.move_pos_world_space(world_x, world_y)
        self.organisms_add_queue.append(organ)

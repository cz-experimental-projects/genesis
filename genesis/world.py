from genesis.organ import Organ


class World:
    organisms: list[Organ]
    organisms_add_queue: list[Organ]

    def update(self) -> None:
        for organism in self.organisms:
            organism.update()

        self.__remove_marked_organisms()
        self.__add_queued_organisms()

    def __remove_marked_organisms(self) -> None:
        self.organisms = [organism for organism in self.organisms if not organism.to_remove]

    def __add_queued_organisms(self) -> None:
        for organism in self.organisms_add_queue:
            self.organisms.append(organism)
        self.organisms_add_queue.clear()

    def draw(self) -> None:
        for organism in self.organisms:
            organism.draw()

    def spawn(self, organ: Organ) -> None:
        self.organisms_add_queue.append(organ)

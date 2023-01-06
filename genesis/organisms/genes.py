from typing import Callable
from pyray import get_frame_time, Color, gui_label, Rectangle, gui_color_picker, gui_slider_bar, gui_dropdown_box
from raylib._raylib_cffi import ffi

from genesis.organisms.organ import Gene, Organ
from genesis.utils.colors import COLOR_WHITE
from genesis.utils.shape import Shape
from genesis.utils.utilities import color_str, color_compare, color_cpy


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

    def __init__(self, organ: Organ, max_maturity: int = 100, on_mature: Callable[[Organ], None] = None, maturity_rate: float = 1):
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
            if self.on_mature is not None:
                self.on_mature(self.organ)

    def draw_gene_details(self, ui) -> None:
        self.current_maturity = gui_slider_bar(ui.full_rect_in_panel(20), "", "", self.current_maturity, 0, self.max_maturity)
        gui_label(ui.full_rect_in_panel(20), "  Maturity: {:.2f}/{:.2f}".format(self.current_maturity, self.max_maturity))
        ui.add_spacing(20)

        self.maturity_rate = gui_slider_bar(ui.full_rect_in_panel(20), "", "", self.maturity_rate, 0,self.max_maturity)
        gui_label(ui.full_rect_in_panel(20), "  Maturity Rate: {:.2f}".format(self.maturity_rate))
        ui.add_spacing(20)


# ColorGene is a Gene that sets the color of an Organ's Shape
class ColorGene(Gene):
    # The color that this Gene sets for the Organ's Shape
    color: Color
    old_color: Color

    def __init__(self, organ: Organ, color: Color = COLOR_WHITE):
        # Initialize the Gene with the organ and dominant attributes
        super().__init__(organ, True)
        # Initialize the color attribute
        self.color = color

    # Set the color of the Organ's Shape when the Gene is initialized
    def initialize(self) -> None:
        if self.organ.shape is None:
            return
        self.old_color = self.organ.shape.color
        self.organ.shape.color = self.color

    def uninitialize(self) -> None:
        if self.organ.shape is None:
            return
        self.organ.shape.color = self.old_color

    def draw_gene_details(self, ui) -> None:
        # Display the color of the organ
        gui_label(ui.full_rect_in_panel(10), "Color: {}".format(color_str(self.color)))
        ui.add_spacing(10)
        color_last_frame = color_cpy(self.color)
        self.color = gui_color_picker(
            Rectangle(ui.relative_to_panel_x(0), ui.relative_to_panel_y(ui.y_level), 60, 60),
            "Color",
            self.color
        )
        ui.add_spacing(60)

        if not color_compare(self.color, color_last_frame):
            self.organ.shape.color = self.color


# ShapeGene is a Gene that sets the Shape of an Organ
class ShapeGene(Gene):
    # The Shape that this Gene sets for the Organ
    shape: Shape

    # Flag for the ui
    selecting_shape: bool

    def __init__(self, organ: Organ, shape: Shape = Shape.empty()):
        # Initialize the Gene with the organ and dominant attributes
        super().__init__(organ, False)
        # Initialize the shape attribute
        self.shape = shape

        shape_types = Shape.__subclasses__()
        try:
            index = shape_types.index(self.shape.__class__)
        except ValueError:
            index = 0

        self.selected_shape = ffi.new("int *", index)
        self.selecting_shape = False

    # Set the Shape of the Organ when the Gene is initialized
    def initialize(self) -> None:
        self.organ.shape = self.shape

    def uninitialize(self) -> None:
        self.organ.shape = None

    def draw_gene_details(self, ui) -> None:
        # Display the shape of the organ
        last_selected = self.selected_shape[0]

        shape_types = Shape.__subclasses__()
        options = ""
        for shape_type in shape_types:
            options += shape_type.__name__ + ";"

        if gui_dropdown_box(ui.full_rect_in_panel(20), options[:-1], self.selected_shape, self.selecting_shape):
            self.selecting_shape = not self.selecting_shape
        ui.add_spacing(20)

        if self.selecting_shape:
            ui.add_spacing(len(shape_types) * 22)

        if self.selected_shape[0] != last_selected:
            self.shape = shape_types[self.selected_shape[0]]()
            self.organ.initialize_genes()

        self.shape.draw_shape_detail_in_ui(ui)


# HungerGene restricts the organ with energy
class EnergyGene(Gene):
    max_energy_level: int
    energy_level: float
    energy_depletion_rate: float

    def __init__(self, organ: Organ, max_energy_level: int = 100, energy_depletion_rate: float = 1):
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

    def draw_gene_details(self, ui) -> None:
        self.energy_level = gui_slider_bar(ui.full_rect_in_panel(20), "", "", self.energy_level, 0,self.max_energy_level)
        gui_label(ui.full_rect_in_panel(20), "  Energy: {:.2f}/{:.2f}".format(self.energy_level, self.max_energy_level))
        ui.add_spacing(20)

        self.energy_depletion_rate = gui_slider_bar(ui.full_rect_in_panel(20), "", "", self.energy_depletion_rate, 0, self.max_energy_level)
        gui_label(ui.full_rect_in_panel(20), "  Depletion Rate: {:.2f}".format(self.energy_depletion_rate))
        ui.add_spacing(20)

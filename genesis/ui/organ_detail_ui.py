from typing import Optional

from pyray import *
from genesis.organisms.organ import Organ
from genesis.ui.expandable_list import ExpandableList


class OrganDetailsUI:
    # The Organ object that is currently being displayed in the panel
    organ: Optional[Organ]

    # The margin on the left side of the panel, in pixels
    margin_left: int
    # The margin on the right side of the panel, in pixels
    margin_right: int
    # The margin at the top of the panel, in pixels
    margin_up: int
    # The margin at the bottom of the panel, in pixels
    margin_down: int

    # The amount of space between each element, in pixels
    spacing: int

    # The width of the panel, in pixels
    panel_w: int
    # The height of the panel, in pixels
    panel_h: int
    # The x-coordinate of the top-left corner of the panel, in pixels
    panel_x: int
    # The y-coordinate of the top-left corner of the panel, in pixels
    panel_y: int

    y_level: int
    captured_y_level: int

    children_organ: ExpandableList
    genes: ExpandableList
    dominant_genes: ExpandableList

    def __init__(self):
        # Initialize the organ attribute to None and the margins, panel dimensions, and expanded_children_organs flag to their default values
        self.organ = None

        self.margin_left = 10
        self.margin_right = 10
        self.margin_up = 5
        self.margin_down = 5
 
        self.spacing = 5

        self.panel_w = 0
        self.panel_h = 0
        self.panel_x = 0
        self.panel_y = 0

        self.y_level = 0

        self.children_organ = ExpandableList("Children Organs", None, None)
        self.genes = ExpandableList("Genes", None, None)
        self.dominant_genes = ExpandableList("Dominant Genes", None, None)

    # noinspection DuplicatedCode
    def render(self):
        def render_children_organ(local_y) -> int:
            # Display the child organs as buttons
            for child_organ in self.organ.children_organs:
                child_rect = Rectangle(
                    self.relative_to_panel_x(40),
                    self.relative_to_panel_y(local_y),
                    self.maximum_width_in_panel() - 40,
                    20
                )

                if gui_button(child_rect, child_organ.__class__.__name__):
                    # Focus on the selected child organ
                    self.organ = child_organ
                    self.children_organ.expanded = False

                local_y += 25
            return local_y

        def render_genes(genes, local_y) -> int:
            for gene in genes:
                child_rect = Rectangle(
                    self.relative_to_panel_x(40),
                    self.relative_to_panel_y(local_y),
                    self.maximum_width_in_panel() - 40,
                    20
                )

                if gui_button(child_rect, gene.__class__.__name__):
                    pass

                local_y += 25
            return local_y

        # Do not render if there is no organ to display details for
        if self.organ is None:
            return

        # Get the screen dimensions
        screen_width = get_screen_width()
        screen_height = get_screen_height()

        # Set the dimensions and position of the panel
        self.panel_w = int(screen_width / 3)
        self.panel_h = screen_height
        self.panel_x = screen_width - self.panel_w
        self.panel_y = 0

        self.y_level = 0

        # Create a panel to display the organ details
        gui_panel(Rectangle(self.panel_x, self.panel_y, self.panel_w, self.panel_h), "Organ Details")

        self.start_box_group()
        # Display the x-coordinate and y-coordinate of the organ
        gui_label(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.5, 10), "World X: {x:.1f}".format(x=self.organ.world_x))
        gui_label(Rectangle(self.relative_to_panel_x(self.maximum_width_in_panel() * 0.5, True), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.5, 10),"World Y: {y:.1f}".format(y=self.organ.world_y))
        self.y_level += 10 + self.spacing

        # Display the x-coordinate and y-coordinate of the organ
        gui_label(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.5, 10), "Local X: {x:.1f}".format(x=self.organ.local_x))
        gui_label(Rectangle(self.relative_to_panel_x(self.maximum_width_in_panel() * 0.5, True), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.5, 10),"Local Y: {y:.1f}".format(y=self.organ.local_y))
        self.y_level += 10 + self.spacing

        # Display the shape of the organ
        gui_label(
            Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 10),
            "Shape: {shape}".format(shape=self.organ.shape.__class__.__name__)
        )
        self.y_level += 10 + self.spacing
        self.end_box_group("Basic Information")

        self.start_box_group()
        # Display a button that is a reference to the parent organ of this organ if present
        if self.organ.parent_organ is not None:
            if gui_button(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 20), "Parent Organ"):
                # Focus on the parent organ
                self.organ = self.organ.parent_organ
            self.y_level += 20 + self.spacing

        # Display an expandable list of all the children organs
        self.children_organ.rect = Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 20)
        self.children_organ.render_callback = render_children_organ
        self.y_level += self.children_organ.render(self.y_level) + self.spacing
        self.end_box_group("Hierarchical Organs")

        self.start_box_group()
        self.genes.rect = Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 20)
        self.genes.render_callback = lambda y: render_genes(self.organ.dna, y)
        self.y_level += self.genes.render(self.y_level) + self.spacing

        self.dominant_genes.rect = Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 20)
        self.dominant_genes.render_callback = lambda y: render_genes(self.organ.dominant_dna, y)
        self.y_level += self.dominant_genes.render(self.y_level) + self.spacing
        self.end_box_group("Genetics")

        self.organ.draw_organ_details(self)

        # Delete button used to remove this organ
        if gui_button(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), 20), "Delete Organ"):
            self.organ.remove()
            self.organ = None if self.organ.parent_organ is None else self.organ.parent_organ

    def relative_to_panel_x(self, x, ignore_margin: bool = False) -> int:
        if ignore_margin:
            return self.panel_x + x
        return self.panel_x + self.margin_left + x

    def relative_to_panel_y(self, y, ignore_margin: bool = False) -> int:
        if ignore_margin:
            return self.panel_y + 30 + y
        return self.panel_y + 30 + self.margin_up + y

    def maximum_width_in_panel(self) -> int:
        return self.panel_w - self.margin_left - self.margin_right

    def mouse_over(self) -> bool:
        from genesis.input import is_mouse_over_screen_space
        return is_mouse_over_screen_space(self.panel_x, self.panel_y, self.panel_w, self.panel_h)

    def start_box_group(self) -> None:
        self.captured_y_level = self.y_level
        self.y_level += self.margin_up * 2
        self.margin_right *= 2
        self.margin_left *= 2

    def end_box_group(self, title: str) -> None:
        self.margin_right *= 0.5
        self.margin_left *= 0.5

        # A group to box the positions and shape
        gui_group_box(
            Rectangle(
                self.relative_to_panel_x(0),
                self.relative_to_panel_y(self.captured_y_level),
                self.maximum_width_in_panel(),
                self.y_level - self.captured_y_level + self.margin_down
            ),

            title)

        self.y_level += self.margin_down + self.spacing * 2
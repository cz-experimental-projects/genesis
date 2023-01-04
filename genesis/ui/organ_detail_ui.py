from typing import Optional

from pyray import *
from genesis.organisms.organ import Organ
from genesis.utils.colors import COLOR_GRAY


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

    # The width of the panel, in pixels
    panel_w: int
    # The height of the panel, in pixels
    panel_h: int
    # The x-coordinate of the top-left corner of the panel, in pixels
    panel_x: int
    # The y-coordinate of the top-left corner of the panel, in pixels
    panel_y: int

    # A flag indicating whether the list of child organs is currently expanded or collapsed
    expanded_children_organs: bool

    def __init__(self):
        # Initialize the organ attribute to None and the margins, panel dimensions, and expanded_children_organs flag to their default values
        self.organ = None

        self.margin_left = 0
        self.margin_right = 20
        self.margin_up = 0
        self.margin_down = 0

        self.panel_w = 0
        self.panel_h = 0
        self.panel_x = 0
        self.panel_y = 0

        self.expanded_children_organs = False

    def render(self):
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

        # Calculate the maximum width of the panel, taking into account the margins
        max_width = self.maximum_width_in_panel()

        # Calculate the half-width of the panel
        half_width = max_width * 0.5
        y_level = 0

        # Create a panel to display the organ details
        gui_panel(Rectangle(self.panel_x, self.panel_y, self.panel_w, self.panel_h), "Organ details")

        # Display the x-coordinate and y-coordinate of the organ
        gui_label(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(y_level), half_width, 10), "X: {x:.1f}".format(x=self.organ.world_x))
        gui_label(Rectangle(self.relative_to_panel_x(half_width), self.relative_to_panel_y(y_level), half_width, 10),"Y: {y:.1f}".format(y=self.organ.world_y))
        y_level += 15

        # Display the shape of the organ
        gui_label(
            Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(y_level), max_width, 10),
            "Shape: {shape}".format(shape=self.organ.shape.__class__.__name__)
        )
        y_level += 15

        # Display a button that is a reference to the parent organ of this organ if present
        if self.organ.parent_organ is not None:
            if gui_button(Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(y_level), max_width, 20), "Parent organ"):
                # Focus on the parent organ
                self.organ = self.organ.parent_organ
                self.expanded_children_organs = False
            y_level += 25

        # Display a button to expand or collapse the child organs of the organ
        gui_draw_icon(GuiIconName.ICON_ARROW_DOWN_FILL if self.expanded_children_organs else GuiIconName.ICON_ARROW_RIGHT_FILL, self.relative_to_panel_x(-2), self.relative_to_panel_y(y_level), 1, COLOR_GRAY)
        if gui_button(Rectangle(self.relative_to_panel_x(16), self.relative_to_panel_y(y_level), max_width - 16, 20), "{collapse_or_expand} Child Organs".format(collapse_or_expand="Collapse" if self.expanded_children_organs else "Expand")):
            self.expanded_children_organs = not self.expanded_children_organs
        y_level += 25

        if self.expanded_children_organs:
            # Display the child organs as buttons
            for i, child_organ in enumerate(self.organ.children_organs):
                child_rect = Rectangle(
                    self.relative_to_panel_x(40),
                    self.relative_to_panel_y(y_level),
                    max_width - 40,
                    20
                )

                if gui_button(child_rect, child_organ.__class__.__name__):
                    # Focus on the selected child organ
                    self.organ = child_organ
                    self.expanded_children_organs = False

                y_level += 25

    def relative_to_panel_x(self, x) -> int:
        return self.panel_x + 7 + self.margin_left + x

    def relative_to_panel_y(self, y) -> int:
        return self.panel_y + 30 + self.margin_up + y

    def maximum_width_in_panel(self) -> int:
        return self.panel_w - self.margin_left - self.margin_right

    def mouse_over(self) -> bool:
        from genesis.input import is_mouse_over_screen_space
        return is_mouse_over_screen_space(self.panel_x, self.panel_y, self.panel_w, self.panel_h)

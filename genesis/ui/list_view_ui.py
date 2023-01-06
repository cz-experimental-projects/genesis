from pyray import *


class ListViewUI:
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

    # Current rendering Y-Level, used to list items in the ui vertically
    y_level: int
    # Captures y level at the moment, used for making box groups
    captured_y_level: int

    def __init__(self):
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
        self.captured_y_level = 0

    def relative_to_panel_x(self, x, ignore_margin: bool = False) -> int:
        if ignore_margin:
            return self.panel_x + x
        return self.panel_x + self.margin_left + x

    def relative_to_panel_x_from_right(self, x, ignore_margin: bool = False) -> int:
        if ignore_margin:
            return self.panel_x + x
        return self.panel_x + self.margin_right + x

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

    def full_rect_in_panel(self, height) -> Rectangle:
        return Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel(), height)

    def half_rect_in_panel_left(self, height) -> Rectangle:
        return Rectangle(self.relative_to_panel_x(0), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.48, height)

    def half_rect_in_panel_right(self, height) -> Rectangle:
        return Rectangle(self.relative_to_panel_x(self.maximum_width_in_panel() * 0.52), self.relative_to_panel_y(self.y_level), self.maximum_width_in_panel() * 0.48, height)

    def add_spacing(self, height) -> None:
        self.y_level += height + self.spacing
from typing import Callable
from pyray import Rectangle, gui_draw_icon, GuiIconName, gui_button
from genesis.utils.colors import COLOR_GRAY


class ExpandableList:
    def __init__(self, rect: Rectangle, render_callback: Callable[[int], None]) -> None:
        self.rect = rect
        self.render_callback = render_callback
        self.expanded = False
        self.item_height = 20

    def render(self, y_offset: int) -> None:
        gui_draw_icon(GuiIconName.ICON_ARROW_DOWN_FILL if self.expanded else GuiIconName.ICON_ARROW_RIGHT_FILL, self.rect.x, self.rect.y, 1, COLOR_GRAY)
        if gui_button(self.rect, "Expand" if self.expanded else "Collapse"):
            self.expanded = not self.expanded
        if self.expanded:
            self.render_callback(y_offset + self.item_height + 5)

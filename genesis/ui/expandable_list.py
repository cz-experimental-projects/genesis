from typing import Callable
from pyray import Rectangle, gui_draw_icon, GuiIconName, gui_button
from genesis.utils.colors import COLOR_GRAY


class ExpandableList:
    list_name: str
    rect: Rectangle
    render_callback: Callable
    expanded: bool

    def __init__(self, list_name: str, rect: Rectangle, render_callback: Callable, ui) -> None:
        self.list_name = list_name
        self.rect = rect
        self.render_callback = render_callback
        self.expanded = False
        self.ui = ui

    def render(self):
        gui_draw_icon(GuiIconName.ICON_ARROW_DOWN_FILL if self.expanded else GuiIconName.ICON_ARROW_RIGHT_FILL, int(self.rect.x - 2), int(self.rect.y), 1, COLOR_GRAY)
        if gui_button(Rectangle(self.rect.x + 16, self.rect.y, self.rect.width - 16, self.rect.height), "{t} {list}".format(t="Collapse" if self.expanded else "Expand", list=self.list_name)):
            self.expanded = not self.expanded

        self.ui.y_level += self.rect.height + self.ui.spacing

        if self.expanded:
            self.ui.margin_left += 30
            self.render_callback()
            self.ui.margin_left -= 30

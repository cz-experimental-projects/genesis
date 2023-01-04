from typing import Callable
from pyray import Rectangle, gui_draw_icon, GuiIconName, gui_button
from genesis.utils.colors import COLOR_GRAY


class ExpandableList:
    list_name: str
    rect: Rectangle
    render_callback: Callable[[int], int]
    expanded: bool

    def __init__(self, list_name: str, rect: Rectangle, render_callback: Callable[[int], int]) -> None:
        self.list_name = list_name
        self.rect = rect
        self.render_callback = render_callback
        self.expanded = False

    def render(self, y_offset: int) -> int:
        gui_draw_icon(GuiIconName.ICON_ARROW_DOWN_FILL if self.expanded else GuiIconName.ICON_ARROW_RIGHT_FILL, int(self.rect.x - 2), int(self.rect.y), 1, COLOR_GRAY)
        if gui_button(Rectangle(self.rect.x + 16, self.rect.y, self.rect.width - 16, self.rect.height), "{t} {list}".format(t="Collapse" if self.expanded else "Expand", list=self.list_name)):
            self.expanded = not self.expanded
        if self.expanded:
            return self.render_callback(y_offset + self.rect.height + 5) - y_offset - 5

        return self.rect.height

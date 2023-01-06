from typing import Optional

from pyray import *
from raylib._raylib_cffi import ffi

from genesis.organisms.organ import Organ, Gene
from genesis.ui.list_view_ui import ListViewUI


class CreateGeneWindow(ListViewUI):
    enabled: bool
    organ: Optional[Organ]

    gene_choice_editing: bool

    def __init__(self):
        super().__init__()
        self.panel_w = 300
        self.panel_h = 250

        self.enabled = False
        self.organ = None

        self.gene_choice = ffi.new("int *", 0)
        self.gene_choice_editing = False

    def render(self):
        if not self.enabled:
            return

        self.panel_x = int((get_screen_width() - self.panel_w) * 0.5)
        self.panel_y = int(get_screen_height() * 0.25)
        self.y_level = 0

        if gui_window_box(Rectangle(self.panel_x, self.panel_y, self.panel_w, self.panel_h), "Create Gene"):
            self.enabled = not self.enabled

        gene_types = Gene.__subclasses__()
        options = ""
        for gene_type in gene_types:
            options += gene_type.__name__ + ";"

        if gui_dropdown_box(self.full_rect_in_panel(20), options[:-1], self.gene_choice, self.gene_choice_editing):
            self.gene_choice_editing = not self.gene_choice_editing
        self.add_spacing(20)

        if self.gene_choice_editing:
            self.add_spacing(len(gene_types) * 22)

        if gui_button(self.full_rect_in_panel(20), "Confirm"):
            gene = gene_types[self.gene_choice[0]](self.organ)
            self.organ.add_gene(gene)

        self.add_spacing(20)
        self.panel_h = self.y_level + 40

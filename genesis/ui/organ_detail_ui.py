from typing import Optional

from pyray import *
from genesis.organisms.organ import Organ, Gene
from genesis.ui.expandable_list import ExpandableList
from genesis.ui.list_view_ui import ListViewUI


class OrganDetailsUI(ListViewUI):
    # The Organ object that is currently being displayed in the panel
    organ: Optional[Organ]

    # Expandable list of child organs
    children_organ: ExpandableList
    # Expandable list of genes
    genes: ExpandableList
    # Expandable list of dominant genes
    dominant_genes: ExpandableList

    def __init__(self):
        super().__init__()
        self.organ = None
        self.children_organ = ExpandableList("Children Organs", None, None, self)
        self.genes = ExpandableList("Genes", None, None, self)
        self.dominant_genes = ExpandableList("Dominant Genes", None, None, self)

    # noinspection DuplicatedCode
    def render(self):
        def render_children_organ():
            # Display the child organs as buttons
            for child_organ in self.organ.children_organs:
                child_rect = Rectangle(
                    self.relative_to_panel_x(0),
                    self.relative_to_panel_y(self.y_level),
                    self.maximum_width_in_panel(),
                    20
                )

                if gui_button(child_rect, child_organ.__class__.__name__):
                    # Focus on the selected child organ
                    self.organ = child_organ
                    self.children_organ.expanded = False

                self.add_spacing(20)

        def render_genes(genes):
            for gene in genes:
                child_rect = Rectangle(
                    self.relative_to_panel_x(0),
                    self.relative_to_panel_y(self.y_level),
                    self.maximum_width_in_panel(),
                    20
                )

                if self.gui_gene_button(child_rect, gene):
                    self.organ.remove_gene(gene)

        # Do not render if there is no organ to display details for
        if self.organ is None:
            return

        if is_key_pressed(KeyboardKey.KEY_DELETE):
            self.delete_organ()
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
        gui_label(self.half_rect_in_panel_left(10), "World X: {x:.1f}".format(x=self.organ.world_x))
        gui_label(self.half_rect_in_panel_right(10),"World Y: {y:.1f}".format(y=self.organ.world_y))
        self.add_spacing(10)

        # Display the x-coordinate and y-coordinate of the organ
        gui_label(self.half_rect_in_panel_left(10), "Local X: {x:.1f}".format(x=self.organ.local_x))
        gui_label(self.half_rect_in_panel_right(10),"Local Y: {y:.1f}".format(y=self.organ.local_y))
        self.add_spacing(10)
        self.end_box_group("Basic Information")

        self.start_box_group()
        # Display a button that is a reference to the parent organ of this organ if present
        if gui_button(self.full_rect_in_panel(20), "Create Child Organ"):
            self.organ.add_child_organ(Organ.blank_organ())
        self.add_spacing(20)

        if self.organ.parent_organ is not None:
            if gui_button(self.full_rect_in_panel(20), "Parent Organ"):
                # Focus on the parent organ
                self.organ = self.organ.parent_organ
            self.add_spacing(20)

        # Display an expandable list of all the children organs
        self.children_organ.rect = self.full_rect_in_panel(20)
        self.children_organ.render_callback = render_children_organ
        self.children_organ.render()
        self.end_box_group("Hierarchical Organs")

        self.start_box_group()
        from genesis import CREATE_GENE_WINDOW
        if gui_button(self.full_rect_in_panel(20), "Add Gene"):
            CREATE_GENE_WINDOW.organ = self.organ
            CREATE_GENE_WINDOW.enabled = True
        self.add_spacing(20)

        self.genes.rect = self.full_rect_in_panel(20)
        self.genes.render_callback = lambda: render_genes(self.organ.dna)
        self.genes.render()

        self.dominant_genes.rect = self.full_rect_in_panel(20)
        self.dominant_genes.render_callback = lambda: render_genes(self.organ.dominant_dna)
        self.dominant_genes.render()
        self.end_box_group("Genetics")

        self.organ.draw_organ_details(self)

        # Delete button used to remove this organ
        if gui_button(self.full_rect_in_panel(20), "Delete Organ"):
            self.delete_organ()

    def gui_gene_button(self, rect: Rectangle, gene: Gene) -> bool:
        size = rect.width * 0.9

        gui_status_bar(Rectangle(
            rect.x,
            rect.y,
            size,
            rect.height
        ), gene.__class__.__name__)

        delete = gui_button(Rectangle(
            rect.x + size + self.spacing,
            rect.y,
            rect.width * 0.1 - self.spacing,
            rect.height
        ), gui_icon_text(GuiIconName.ICON_FILE_DELETE, ""))

        self.add_spacing(rect.height)

        self.margin_left += 30
        gene.draw_gene_details(self)
        self.margin_left -= 30

        return delete

    def delete_organ(self):
        self.organ.remove()
        self.organ = None if self.organ.parent_organ is None else self.organ.parent_organ

import sys

from pyray import *

from genesis.ui.create_gene_ui import CreateGeneWindow
from genesis.ui.organ_detail_ui import OrganDetailsUI
from genesis.utils.colors import BACKGROUND_COLOR, BACKGROUND_SCROLL_COLOR
from genesis.world import World

# Set the window to be resizable
set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)

# Initialize the window with a size of 800x450 and a title of "Genesis"
init_window(1400, 860, "Genesis")

# Disable escape quitting the window
set_exit_key(KeyboardKey.KEY_NULL)

# Camera zoom values
MAXIMUM_ZOOM = 5
MINIMUM_ZOOM = 0.8

# Camera panning
prev_mouse_position = get_mouse_position()

# Create a World object and a Camera2D object
WORLD: World = World()
CAMERA: Camera2D = Camera2D(Vector2(get_screen_width() * 0.5, get_screen_height() * 0.5), vector2_zero(), 0, 1)
ORGAN_DETAIL_UI: OrganDetailsUI = OrganDetailsUI()
CREATE_GENE_WINDOW: CreateGeneWindow = CreateGeneWindow()

# Import handle_input here as it references the WORLD and CAMERA object
from input import handle_input


def render_ui():
    # Draw the FPS (frames per second) in the top left corner of the screen
    draw_fps(5, 5)
    ORGAN_DETAIL_UI.render()
    CREATE_GENE_WINDOW.render()


def render_world():
    # Update the game world
    WORLD.update()
    # Draw the game world
    WORLD.draw(ORGAN_DETAIL_UI)


scrolling_bg_x: float = 0.0
scrolling_bg_y: float = 0.0
bg_tex = load_texture("../resources/noise.png")

# Run the game loop
while not window_should_close():
    # Start drawing to the window
    begin_drawing()

    # Clear the background to white
    clear_background(BACKGROUND_COLOR)

    # Renders the background
    scrolling_bg_x -= 0.008
    scrolling_bg_y -= 0.005
    if scrolling_bg_x <= -bg_tex.width*2:
        scrolling_bg_x = 0

    if scrolling_bg_y <= -bg_tex.height*2:
        scrolling_bg_y = 0

    draw_texture_ex(bg_tex, Vector2(scrolling_bg_x, scrolling_bg_y), 0.0, 4, BACKGROUND_SCROLL_COLOR)
    draw_texture_ex(bg_tex, Vector2(bg_tex.width * 4 + scrolling_bg_x, scrolling_bg_y), 0.0, 4, BACKGROUND_SCROLL_COLOR)

    # Handle user input
    handle_input()

    # Set the camera for 2D rendering
    begin_mode_2d(CAMERA)

    # Renders in world elements
    render_world()

    # Reset the camera and stop drawing to the window
    end_mode_2d()

    # Renders the UI after world so ui elements won't be affected by camera and will be on top of the world elements movement
    render_ui()

    end_drawing()

# Close the window when the game loop ends
close_window()
sys.exit()

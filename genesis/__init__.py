# Import the pyray module
import sys

from pyray import *

# Import World class from the genesis package
from genesis.world import World

# Set the window to be resizable
set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)

# Initialize the window with a size of 800x450 and a title of "Genesis"
init_window(800, 450, "Genesis")

# Camera zoom values
MAXIMUM_ZOOM = 5
MINIMUM_ZOOM = 0.8

# Camera panning
prev_mouse_position = get_mouse_position()

# Create a World object and a Camera2D object
WORLD: World = World()
CAMERA: Camera2D = Camera2D(Vector2(get_screen_width() * 0.5, get_screen_height() * 0.5), vector2_zero(), 0, 1)

# Import handle_input here as it references the WORLD and CAMERA object
from input import handle_input


def render_ui():
    # Draw the FPS (frames per second) in the top left corner of the screen
    draw_fps(5, 5)


def render_world():
    # Update the game world
    WORLD.update()
    # Draw the game world
    WORLD.draw()


# Run the game loop
while not window_should_close():
    # Start drawing to the window
    begin_drawing()

    # Clear the background to white
    clear_background(GRAY)

    # Handle user input
    handle_input()

    # Renders the UI before setting up camera so ui elements won't be affected by camera movement
    render_ui()

    # Set the camera for 2D rendering
    begin_mode_2d(CAMERA)

    # Renders in world elements
    render_world()

    # Reset the camera and stop drawing to the window
    end_mode_2d()
    end_drawing()

# Close the window when the game loop ends
close_window()
sys.exit()

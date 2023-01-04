from pyray import *

import genesis
from genesis import WORLD, CAMERA, MAXIMUM_ZOOM, MINIMUM_ZOOM
from genesis.organisms.genes import ColorGene, ShapeGene
from genesis.organisms.organ import Organ
from genesis.utils.shape import RectangleShape


# Handle input from the user
def handle_input() -> None:
    # If the T key is pressed, spawn an organ at the mouse position
    if is_key_pressed(KeyboardKey.KEY_T):
        spawn_at_mouse(Organ([
            lambda organ: ColorGene(RED, organ),
            lambda organ: ShapeGene(RectangleShape(10, 10), organ)
        ]))

    # Zooming camera
    mouse_wheel_value = get_mouse_wheel_move()
    camera_zoom = CAMERA.zoom

    if mouse_wheel_value != 0:
        camera_zoom += mouse_wheel_value * 0.5
        CAMERA.zoom = clamp(camera_zoom, MINIMUM_ZOOM, MAXIMUM_ZOOM)

    # Panning camera
    thisPos = get_mouse_position()
    delta = vector2_subtract(genesis.prev_mouse_position, thisPos)
    genesis.prev_mouse_position = thisPos

    if is_mouse_button_down(0):
        CAMERA.target = get_screen_to_world_2d(vector2_add(CAMERA.offset, delta), CAMERA);


# Spawn an organ at the mouse position in the world
def spawn_at_mouse(organ: Organ) -> None:
    WORLD.spawn_with_vec2(organ, get_mouse_world_position())


# Get the world position of the mouse
def get_mouse_world_position() -> Vector2:
    return get_screen_to_world_2d(get_mouse_position(), CAMERA)


# Get the screen position of the mouse
def get_mouse_position() -> Vector2:
    return Vector2(get_mouse_x(), get_mouse_y())


# Check if mouse is over an area in world space
def is_mouse_over_world_space(x, y, width, height) -> bool:
    mouse_pos = get_mouse_world_position()
    return x < mouse_pos.x < x + width and y < mouse_pos.y < y + height

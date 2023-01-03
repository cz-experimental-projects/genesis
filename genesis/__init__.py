from pyray import *
from genesis.world import World

set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
init_window(800, 450, "Genesis")

WORLD: World = World()

while not window_should_close():
    begin_drawing()

    clear_background(WHITE)
    draw_fps(5, 5)

    WORLD.update()
    WORLD.draw()

    end_drawing()

close_window()

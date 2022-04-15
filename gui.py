from unigui import UniGui

WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
NUM_COLORS = 2

gui = UniGui(WIDTH, HEIGHT, scale_factor=SCALE_FACTOR)
gui.set_title("hello carsten")
gui.set_main_area()
gui.set_icon()

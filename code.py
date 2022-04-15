### An attempt to get Blinka Displayio working on Generic x86 PC

import time

from pygame_display import PygameDisplay
from unigui import UniGui

WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
NUM_COLORS = 2

gui = UniGui(WIDTH, HEIGHT, scale_factor=SCALE_FACTOR)
gui.set_title("hello carsten")
gui.set_main_area()

print("starting...")

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)

gui.update(display)

while(1):
    pass
    # x = randint(0, 150)
    # y = randint(50, 250)
    # ta.x = x
    # ta.y = y
    # display.show(ta)
    time.sleep(0.1)
    event = display.refresh()
    if event == 1:
        gui.set_main_area()
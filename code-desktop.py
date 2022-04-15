### An attempt to get Blinka Displayio working on Generic x86 PC

import time
from pygame_display import PygameDisplay
from gui import gui, WIDTH, HEIGHT, SCALE_FACTOR

print("starting...")

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)

gui.update(display)

while(1):
    time.sleep(0.1)
    event = display.refresh()
    if event == 1:
        gui.set_main_area()
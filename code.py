### An attempt to get Blinka Displayio working on Generic x86 PC

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

import time
import sys
from pygame_display import PygameDisplay

from random import randint

WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
NUM_COLORS = 2

font_file = "fonts/Silom-Bold-24.bdf"
font = bitmap_font.load_font(font_file)

BLACK      = 0x000000
LIGHT_GRAY = 0x707070
DARK_GRAY  = 0x454545
RED        = 0xFF0000

ta = label.Label(font, text="hello", color=RED)
ta.x = 50
ta.y = 50

splash = displayio.Bitmap(WIDTH, HEIGHT, NUM_COLORS)
palette = displayio.Palette(NUM_COLORS)
palette[0] = BLACK
palette[1] = LIGHT_GRAY

for x in range(WIDTH):
    for y in range(HEIGHT):
        splash[x, y] = 0 #round((x + y) / 10) % 2

tg = displayio.TileGrid(splash, pixel_shader=palette)
root = displayio.Group(scale=SCALE_FACTOR)
root.append(tg)
root.append(ta)

print("starting...")

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)

display.show(root)

while(1):
    # x = randint(0, 150)
    # y = randint(50, 250)
    # ta.x = x
    # ta.y = y
    display.show(ta)
    time.sleep(0.1)
    display.refresh()
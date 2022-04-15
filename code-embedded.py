### An attempt to get Blinka Displayio working on Generic x86 PC

import time
import board
from displayio import FourWire
from adafruit_ili9341 import ILI9341
from gui import gui, WIDTH, HEIGHT, SCALE_FACTOR

print("starting...")

# HW pins for Raspberry Pi and PiTFT
spi      = board.SPI()
tft_cs   = board.CE0
tft_dc   = board.D25
tft_rst  = board.D24
BAUDRATE = 24000000
display_bus = FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_rst,
    baudrate=BAUDRATE,
)

display = ILI9341(display_bus, width=WIDTH, height=HEIGHT)

gui.update(display)

while(1):
    time.sleep(0.1)
    event = display.refresh()
    if event == 1:
        gui.set_main_area()
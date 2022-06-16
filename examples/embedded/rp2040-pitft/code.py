"""
This is a CircuitPython script to test UniGui functionality on an RP2040
connected to a PiTFT 2.8" + Capacitive Touch Display
    gui.py contains the UniGui code
"""

import time
import board
import displayio
from adafruit_ili9341 import ILI9341
from gui import gui, toolbar_widget, WIDTH, HEIGHT, SCALE_FACTOR
# from unigui.widget import resource_filename, print_resource_path

print("starting UniGui demo...")

# HW pins for PiTFT 2.8" Plus Capacitive Touch with Feather RP2040
displayio.release_displays()
spi      = board.SPI()
tft_cs   = board.D4
tft_dc   = board.D25
tft_rst  = board.D24
BAUDRATE = 24000000
display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_rst,
    baudrate=BAUDRATE,
)

display = ILI9341(
    display_bus,
    width=WIDTH,
    height=HEIGHT,
    rotation=180,
)

gui.update(display)

while True:
    toolbar_widget.set_value(str(time.monotonic()))
    time.sleep(1)

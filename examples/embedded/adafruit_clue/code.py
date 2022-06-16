import gc

import time
import board
import digitalio
# from adafruit_clue import clue
from audio import Mic
from climate import Climate

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from gui import gui

print("Hello from CircuitPython on CLUE!")

# BLE Configuration
print("Starting up BLE advertising...")
gc.collect()
print("Free memory before BLE calls: {}".format(gc.mem_free()))
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.start_advertising(advertisement)
gc.collect()
print("Free memory after BLE calls: {}".format(gc.mem_free()))

# UniGui Configuration
display = board.DISPLAY
gc.collect()
print("Free memory before UniGui calls: {}".format(gc.mem_free()))
# CS = Solarized.dark
# # gui = UniGui(display.width, display.height, colorscheme=CS)
# splash = displayio.Group()
# # gui.border_on()
# title = TextWidget(
#     "title",
#     0,
#     0,
#     display.width,
#     20,
#     colorscheme=CS,
#     # font_path='fonts/SNES-Italic-24.bdf',
# )
# title.border_on()
# title.scale = 2
# gc.collect()
# print("Free memory after title creation: {}".format(gc.mem_free()))
# gui.add_widget(title)

# body = TextWidget(
#     "body",
#     0,
#     60,
#     display.width,
#     180,
#     colorscheme=CS,
# )
# body.set_value("testing the text stuff...", h_justification="left", v_justification="top")
# gui.add_widget(body)

# graph = GraphWidget(
#     "graph",
#     0,
#     40,
#     display.width,
#     display.height-40,
#     colorscheme=CS,
# )
# graph.set_x_range(0, 10)
# graph.set_y_range(0, 100)
# print(graph.y_scale)
# graph.draw()

# gc.collect()
# print("Free memory after UniGui calls: {}".format(gc.mem_free()))
# splash.append(title)
# splash.append(body)
# splash.append(graph)

display.show(gui)

# IO Pin Configuration
button_a = digitalio.DigitalInOut(board.BUTTON_A)
button_a.switch_to_input(pull=digitalio.Pull.UP)
white_leds = digitalio.DigitalInOut(board.WHITE_LEDS)
white_leds.switch_to_output()

# Sensor Configuration
mic = Mic()
climate = Climate()

start_time = time.monotonic()
dt_100mHz = [10, start_time]
dt_1hz  = [1,   start_time]
dt_2hz  = [0.5, start_time]
dt_10hz = [0.1, start_time]
while True:

    # Continuous Activity
    white_leds.value = not button_a.value
    temp = climate.get_temperature(units="F")
    hum  = climate.get_humidity()
    pres = climate.get_pressure()

    ### Period activity ###
    t = time.monotonic()
    # 0.1Hz
    if t - dt_100mHz[1] > dt_100mHz[0]:
        dt_100mHz[1] = t
        # graph.add_value((t-start_time, mic.sound_level()))

    # 1 Hz
    if t - dt_1hz[1] > dt_1hz[0]:
        dt_1hz[1] = t
        # print("mic value: {}".format(mic.sound_level()))
        climate_string = "Climate: [{:3.1f} F, {:2.1f}% RH, {:4.1f} hPa]".format(
            temp,
            hum,
            pres,
        )
        print(climate_string)
        uart.write(climate_string.encode('utf-8'))
        
    # 2 Hz
    if t - dt_2hz[1] > dt_2hz[0]:
        dt_2hz[1] = t
        s = "{:3.1f} F".format(temp)
        s = s + ("   %d" % mic.sound_level())
        # title.set_value(s, h_justification="left", v_justification="center")
        # graph.add_value((t-start_time, mic.sound_level()))
        # print("    2hz")

    # 10 Hz
    if t - dt_10hz[1] > dt_10hz[0]:
        dt_10hz[1] = t
        # print("  10hz")
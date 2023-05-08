import displayio
from unigui.pygamedisplay import PygameDisplay

import time
import os
import psutil

proc = psutil.Process(os.getpid())

WIDTH = 500
HEIGHT = 500
SCALE_FACTOR = 1

display  = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
my_display_group = displayio.Group()

# display.show merely switches the default group, so doesn't really do much work other
# than setting a class variable.
prev_time = proc.cpu_times()
display.show(my_display_group)
curr_time = proc.cpu_times()
print(f"time for 'display.show(...)' is {sum(curr_time)-sum(prev_time):.5f}")

# display.refresh, on the other hand, does all the drawing and the CPU time seems 
# to increase with the number of pixels of the display
prev_time = curr_time
while True:
    curr_time = proc.cpu_times()
    display.refresh()
    display.get_mouse_clicks()
    print(f"time for refresh and get_mouse_clicks is {sum(curr_time)-sum(prev_time):.5f}")
    prev_time = curr_time
    time.sleep(0.1)
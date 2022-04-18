### An attempt to get Blinka Displayio working on Generic x86 PC

import time
from pygame_display import PygameDisplay
from gui import gui, WIDTH, HEIGHT, SCALE_FACTOR

print("starting...")

display  = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
msgs = gui.get_widget("messages")

gui.update(display)

message = "hello sweet, oh bittersweet world....."
titles = ["hello", "Hello, Carsten"]
border = True
i = j = 0
t0 = time.time()
while(1):
    # Common refresh
    display.refresh()

    # Things todo on click
    click = display.get_mouse_clicks()
    if click is not None:
        print(gui.__len__())
        print("click: " + str(click))
        gui.process_click(click)

    # timed functions go here
    t1 = time.time()
    if (t1 - t0) > 0.05:
        t0 = t1
        j += 1
        msgs.set_value(message[0:(j%len(message))])


   



        



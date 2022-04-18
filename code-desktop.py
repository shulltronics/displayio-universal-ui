### An attempt to get Blinka Displayio working on Generic x86 PC

import time
from pygame_display import PygameDisplay
from gui import gui, WIDTH, HEIGHT, SCALE_FACTOR

print("starting...")

display  = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)

gui.update(display)

message = "hello sweet, oh bittersweet world..."
titles = ["hello", "carsten"]
border = True
i = 0
t0 = time.time()
while(1):
    display.refresh()
    click = display.get_mouse_clicks()
    if click is not None:
        print(click)
        border = not border
        #gui.set_border(border)
        #gui.set_main_area()
        i += 1
        try:
            gui.get_widget("toolbar").set_value(titles[i%2])
            gui.get_widget("messages").set_value(message[0:(i%len(message))])
        except:
            print("Oops! couldn't find widget")
    else:
        pass

    t1 = time.time()
    if (t1 - t0) > 1:
        t0 = t1
        gui.set_icon()



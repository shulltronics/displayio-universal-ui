### An attempt to get Blinka Displayio working on Generic x86 PC

from unigui.pygamedisplay import PygameDisplay
from gui import gui, WIDTH, HEIGHT, SCALE_FACTOR
import time

print("starting...")

display  = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
toolbar = gui.get_widget("toolbar")
msgs = gui.get_widget("messages")
graphics = gui.get_widget("graphics")
button = gui.get_widget("button")
icon = gui.get_widget("icon")
icon.set_click_action(display.quit)

gui.update(display)

message = "hello sweet, oh bittersweet world....."
message2 = "UniGui is a very cool framework"
titles = ["hello", "Hello, Carsten"]
border = True
i = j = k = 0
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
    if (t1 - t0) > 0.15:
        t0 = t1
        j += 1
        k += 0.7
        msgs.set_value(message[0:(j%len(message))])
        toolbar.set_value(str(time.strftime("%H:%M:%S")))
        button.set_value(message2[0:round(k)%len(message2)], h_justification='center', v_justification='center')
        graphics.set_main_area((0, 0))


   



        



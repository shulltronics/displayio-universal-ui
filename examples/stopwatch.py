from unigui import UniGui, TextWidget, PygameDisplay
import time

# Configuration constants
WIDTH = 128
HEIGHT = 64
SCALE_FACTOR = 2

# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale=SCALE_FACTOR)

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget("toolbar", 0, 0, WIDTH, HEIGHT)
gui.add_widget(toolbar_widget)

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
gui.update(display)

running = False
start_time = 0

while True:
    display.refresh()
    click = display.get_mouse_clicks()
    if click is not None:
        # if the clock wasn't running (but now will be), reset the start time
        if running == False:
            start_time = time.time()
        running = not running
        gui.process_click(click)

    if running:
        dt = time.time() - start_time
        toolbar_widget.set_value("%1.2f" %dt)
    
    time.sleep(0.05)
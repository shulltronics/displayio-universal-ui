from unigui import UniGui, TextWidget
from unigui.pygamedisplay import PygameDisplay
from unigui.colorscheme import VSCode, Solarized
import time

# Configuration constants
WIDTH = 128
HEIGHT = 64
SCALE_FACTOR = 2
CS = Solarized.dark

# The main UniGui object
gui = UniGui(
    WIDTH,
    HEIGHT,
    scale=SCALE_FACTOR,
    colorscheme=CS
)

# Setup a full screen text widget
toolbar_widget = TextWidget(
    "toolbar",
    0,
    0,
    WIDTH,
    HEIGHT,
    colorscheme=CS
)
toolbar_widget.border_on()
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
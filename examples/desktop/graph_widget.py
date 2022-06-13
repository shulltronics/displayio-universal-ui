from unigui import UniGui, TextWidget, GraphWidget
from unigui.pygamedisplay import PygameDisplay
from unigui.colorscheme import VSCode, Solarized
import time

# Configuration constants
WIDTH = 240     # Same as CLUE
HEIGHT = 240
SCALE_FACTOR = 2
CS = Solarized.dark

# The main UniGui object
gui = UniGui(
    WIDTH,
    HEIGHT,
    scale=SCALE_FACTOR,
    colorscheme=CS
)

title = TextWidget(
    "title",
    0,
    0,
    WIDTH,
    20,
    colorscheme=CS,
    # font_path='fonts/SNES-Italic-24.bdf',
)
title.set_value("hello", h_justification='left', v_justification='top')
title.border_on()
title.scale = 2
gui.add_widget(title)

graph_widget = GraphWidget(
    "toolbar",
    0,
    40,
    WIDTH,
    HEIGHT-40,
    colorscheme=CS
)
graph_widget.draw()
graph_widget.add_value((50, 50))
gui.add_widget(graph_widget)

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
gui.update(display)

running = False
t0 = time.monotonic()

while True:
    display.refresh()
    click = display.get_mouse_clicks()
    if click is not None:
        t1 = time.monotonic()
        dt = t1 - t0
        graph_widget.add_value((dt, 50))
        print("values: {}".format(graph_widget.values))
    
    time.sleep(0.05)
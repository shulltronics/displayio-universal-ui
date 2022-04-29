from unigui import UniGui
from unigui import IconWidget, Widget, TextWidget, GraphicsWidget, Solarized, VSCode, Shulltronics
import time

# Configuration constants
WIDTH = 640
HEIGHT = 480
SCALE_FACTOR = 2
CS = Shulltronics.dark

# The main UniGui object
gui = UniGui(
    WIDTH,
    HEIGHT,
    scale=SCALE_FACTOR,
    colorscheme=CS
)
# gui.border_on()

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget(
    "toolbar",
    0,
    0,
    WIDTH,
    32,
    TextWidget.LARGE_FONT,
    colorscheme=CS,
)
# gui.add_widget(toolbar_widget)
toolbar_widget.border_on()
toolbar_widget.set_value(str(time.strftime("%H:%M:%S")))
gui.add_widget(toolbar_widget)

icon = IconWidget("icon", WIDTH-32, 0)
# icon.border_off()
gui.add_widget(icon)

# Setup a messages widget that writes text to a predefined area
message_widget = TextWidget("messages", 0, 32, round(WIDTH/2), HEIGHT-128-32, TextWidget.SMALL_FONT)
message_widget.border_on()
gui.add_widget(message_widget)

# Setup a button
button = TextWidget("button", round(WIDTH/2), 32, round(WIDTH/2), HEIGHT-128-32, TextWidget.SMALL_FONT)
button.border_on()
gui.add_widget(button)

# setup a graphics widget
graphics_widget = GraphicsWidget("graphics", 0, HEIGHT-128, WIDTH, 128)
graphics_widget.border_on()
graphics_widget.set_click_action(graphics_widget.set_main_area)
gui.add_widget(graphics_widget)
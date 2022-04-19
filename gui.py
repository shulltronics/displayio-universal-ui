from unigui import UniGui
from widget import Widget, TextWidget, GraphicsWidget, Solarized

# Configuration constants
WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 3
NUM_COLORS = 8

# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale=SCALE_FACTOR)
gui.border_on()

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget("toolbar", 0, 0, WIDTH, 32, TextWidget.LARGE_FONT)
toolbar_widget.border_on()
toolbar_widget.set_value("not default")
gui.add_widget(toolbar_widget)

# Setup a messages widget that writes text to a predefined area
message_widget = TextWidget("messages", 0, 32, round(WIDTH/2), 64, TextWidget.SMALL_FONT)
message_widget.border_on()
# message_widget.set_value("testing")
gui.add_widget(message_widget)

# Setup a button
button = Widget("button", 0, 96, 32, 32)
button.border_on()
gui.add_widget(button)

# setup a graphics widget
graphics_widget = GraphicsWidget("graphics", 0, HEIGHT-128, 128, 128)
graphics_widget.border_on(color_idx=7)
graphics_widget.set_click_action(graphics_widget.set_main_area)
gui.add_widget(graphics_widget)
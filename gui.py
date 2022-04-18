from unigui import UniGui, TextWidget, Solarized

# Configuration constants
WIDTH = 600
HEIGHT = 320
SCALE_FACTOR = 3
NUM_COLORS = 2

# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale_factor=SCALE_FACTOR)
gui.set_border(True)

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget("toolbar", 0, 0, WIDTH, 32, TextWidget.LARGE_FONT)
toolbar_widget.set_border(False)
gui.add_widget(toolbar_widget)

message_widget = TextWidget("messages", 0, 200, WIDTH, 40, TextWidget.SMALL_FONT)
message_widget.set_color(Solarized.GREEN)
message_widget.set_value("testing")
message_widget.set_border(True)
gui.add_widget(message_widget)

#gui.set_main_area()
#gui.set_icon()

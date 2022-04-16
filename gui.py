from unigui import UniGui, TextWidget, Solarized

WIDTH = 800
HEIGHT = 600
SCALE_FACTOR = 2
NUM_COLORS = 2

gui = UniGui(WIDTH, HEIGHT, scale_factor=SCALE_FACTOR)
gui.set_border(True)

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget("toolbar", 0, 0, WIDTH, 32)
toolbar_widget.set_border(False)
gui.add_widget(toolbar_widget)

message_widget = TextWidget("messages", 0, 200, WIDTH, 40, TextWidget.SMALL_FONT)
message_widget.set_color(Solarized.GREEN)
message_widget.set_value("testing")
message_widget.set_border(False)
gui.add_widget(message_widget)

#gui.set_main_area()
#gui.set_icon()

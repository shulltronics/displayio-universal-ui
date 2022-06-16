from unigui import UniGui
from unigui.widget import IconWidget, Widget, TextWidget, GraphicsWidget
from unigui.colorscheme import Solarized, VSCode, Shulltronics
import displayio
import time

# Configuration constants
WIDTH = 240
HEIGHT = 240
SCALE_FACTOR = 1
CS = VSCode.dark

# TODO: Make parent UniGui class not be a full sized bitmap..
#       it takes too much RAM!
gui = displayio.Group()

# Setup a toolbar full width and 32 px high
toolbar_widget = TextWidget(
    "toolbar",
    0,
    0,
    WIDTH,
    HEIGHT,
    font_path=TextWidget.LARGE_FONT,
    colorscheme=CS,
)
toolbar_widget.border_on()
toolbar_widget.set_click_action(toolbar_widget.border_toggle)
toolbar_widget.set_value(str(time.monotonic()))
gui.append(toolbar_widget)
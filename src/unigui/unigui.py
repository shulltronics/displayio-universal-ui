# A GUI framework built upon Adafruit displayio and the widget idea
# This file should not use an platform-dependent code, so that
# it can be run on any platform.
# The user will define the display for their platform as follows:
# GENERIC_PC (Windows or Linux), use PygameDisplay
# Raspberry Pi or Microcontroller, use appropriate display_bus and Display

# These will be re-exported to our package namespace
from unigui.widget import *
from unigui.colorscheme import *
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from random import randint
import math


class UniGui(Widget):
    """
    This is the base class for my GUI
    An instance represents the root window with the following properties:
        * always located at 0, 0
        * size is defined upon creation, and can be scaled up by integer increments
        * has a colorscheme that is stored as a palette
        * TODO has a border that can be turned on or off
    """
    def __init__(self, width, height, colorscheme, scale=1):
        super().__init__(
            "UniGui",
            0,
            0,
            width,
            height,
            colorscheme,
            scale=scale,
        )
        self.widgets = []
        self.set_background()

    def add_widget(self, widget):
        # TODO: first validate the layout?

        # If we didn't override the widget's colorscheme, set it here
        if widget.palette is None:
            widget.palette = self.palette
        self.widgets.append(widget)
        self.append(widget)

    # returns the Widget named <name>, or None
    def get_widget(self, name):
        match = None
        for widget in self.widgets:
            if widget.name == name:
                match = widget
        return match

    # This method makes sure that the widgets don't overlap
    def validate_layout(self):
        for widget in self.widgets:
            pass  #TODO

    # Show the GUI on the display
    def update(self, display):
        display.show(self)

    # Process a click at display location (x, y)
    # We must account for screen scaling in this method
    def process_click(self, click_pos):
        (_x, _y) = click_pos
        x = round(_x / self.scale)
        y = round(_y / self.scale)
        print("(" + str(x) + ", " + str(y) + ")")
        for widget in self.widgets:
            widget_idx = self.index(widget)
            x_min = widget.x
            x_max = widget.x + widget.width
            y_min = widget.y
            y_max = widget.y + widget.height
            contains_x = (x >= x_min) and (x < x_max)
            contains_y = (y >= y_min) and (y < y_max)
            if contains_x and contains_y and widget.clickable:
                print("Widget index " + str(widget_idx) + " is a match! " + "Doing callback...")
                relative_click_pos = (x - widget.x, y - widget.y)
                widget.callback(relative_click_pos)

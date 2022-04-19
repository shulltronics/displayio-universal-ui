# A GUI framework built upon Adafruit displayio and the widget idea
# This file should not use an platform-dependent code, so that
# it can be run on any platform.
# The user will define the display for their platform as follows:
# GENERIC_PC (Windows or Linux), use PygameDisplay
# Raspberry Pi or Microcontroller, use appropriate display_bus and Display

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from widget import Widget, Solarized, VSCode
from random import randint
import math

"""
This is the base class for my GUI
An instance represents the root window with the following properties:
    * always located at 0, 0
    * size is defined upon creation, and can be scaled up by integer increments
    * has a colorscheme that is stored as a palette
    * TODO has a border that can be turned on or off
"""
class UniGui(displayio.Group):

    def __init__(self, width, height, scale=1):
        super().__init__(scale=scale)
        self.x             = 0
        self.y             = 0
        self.width         = width
        self.height        = height
        self.palette       = VSCode.dark
        self.bg_color      = Solarized.BASE03
        self.text_color    = Solarized.BASE3
        self.widgets       = []
        self.border_color  = Solarized.VIOLET
        self.background_bm = None
        self.background_tg = None
        self.set_background()

    def set_background(self, bg_color_index=0):
        bg_bitmap = displayio.Bitmap(self.width, self.height, 8)
        bg_bitmap.fill(bg_color_index)
        self.background_bm = bg_bitmap
        self.background_tg = displayio.TileGrid(bg_bitmap, pixel_shader=self.palette)
        self.append(self.background_tg)

    # returns the tuple: (index, tilegrid) or None
    def get_background_tilegrid(self):
        try:
            idx = self.index(self.background_tg)
            return (idx, self.pop(idx))
        except:
            print("Tried to get non-existant background tilegrid!")
            return None

    def border_on(self, color_idx=7):
        bm = self.background_bm
        # get the index of the background tilegrid.
        # Don't care about the tg itself because we're making a new one
        (tg_index, _) = self.get_background_tilegrid()
        for x in range(0, bm.width):
            bm[x, 0]           = color_idx
            bm[x, bm.height-1] = color_idx
        for y in range(0, bm.height):
            bm[0, y]          = color_idx
            bm[bm.width-1, y] = color_idx
        self.background_tg = displayio.TileGrid(bm, pixel_shader=self.palette)
        self.insert(tg_index, self.background_tg)

    def border_off(self):
        bm = self.background_bm
        # get the index of the background tilegrid.
        # Don't care about the tg itself because we're making a new one
        (tg_index, _) = self.get_background_tilegrid()
        bm.fill(0)
        self.background_tg = displayio.TileGrid(bm, pixel_shader=self.palette)
        self.insert(tg_index, self.background_tg)

    # TODO: clean this up so we modify existing group, not add another
    def set_icon(self):
        icon = displayio.OnDiskBitmap('images/256x32/color_blocks.bmp')
        # icon_tg = displayio.TileGrid(icon, pixel_shader=icon.pixel_shader, width=1, height=1, tile_width=32, tile_height=32)
        for i in range(6):
            icon_tg = displayio.TileGrid(icon, pixel_shader=icon.pixel_shader, width=1, height=1, tile_width=32, tile_height=32)
            icon_tg[0] = randint(0, 5)
            icon_tg.x = 32*i
            icon_tg.y = 32
            self.append(icon_tg)

    def add_widget(self, widget):
        # TODO: first validate the layout
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
                widget.callback()
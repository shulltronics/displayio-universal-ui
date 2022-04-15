# A GUI framework built upon Adafruit displayio and the widget idea
# This file should not use an platform-dependent code, so that
# it can be run on any platform.
# The user will define the display for their platform as follows:
# GENERIC_PC (Windows or Linux), use PygameDisplay
# Raspberry Pi or Microcontroller, use appropriate display_bus and Display

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
from random import randint
import math

class UniGui(displayio.Group):

    WHITE      = 0xFFFFFF
    BLACK      = 0x000000
    LIGHT_GRAY = 0x707070
    DARK_GRAY  = 0x454545
    RED        = 0xFF0000
    GREEN      = 0x00FF00
    BLUE       = 0x0000FF
    MAGENTA    = 0xFF00FF

    def __init__(self, width, height, scale_factor=1):
        self._width      = width
        self._height     = height
        self._bg_color   = self.WHITE
        self._text_color = self.DARK_GRAY
        super().__init__(scale=scale_factor)
        frame = Rect(0, 0, self._width, self._height, fill=self.BLACK, outline=self.MAGENTA)
        self.append(frame)

    def set_title(self, title_msg):
        font_file = "fonts/Silom-Bold-24.bdf"
        font = bitmap_font.load_font(font_file)
        text_area = label.Label(font, text=title_msg, color=self.DARK_GRAY)

        # setup some properties
        text_area.base_alignment = True
        text_area.anchor_point = (0, 0)
        bb = text_area._bounding_box
        (w, h) = (bb[2] - bb[0], bb[3] - bb[1])
        (x, y) = (round(self._width/2) - round(w/2), 0)
        text_area.anchored_position = (x, y)
        frame = Rect(x, y, w, h, fill=self.BLACK, outline=self.RED)

        # Add all the elements together
        self.append(frame)
        self.append(text_area)
        self._title = text_area

    def get_title(self):
        return self._title

    # Draws a triangle centered in the GUI
    def set_main_area(self):
        r = 80
        (offset_x, offset_y) = (round(self._width/2), round(self._height/2))
        # Get three random angles around our circle:
        p0_angle = math.radians(randint(0, 360))
        p1_angle = math.radians(randint(0, 360))
        p2_angle = math.radians(randint(0, 360))
        (x0, y0) = (round(r*math.sin(p0_angle)) + offset_x, round(r*math.cos(p0_angle)) + offset_y)
        (x1, y1) = (round(r*math.sin(p1_angle)) + offset_x, round(r*math.cos(p1_angle)) + offset_y)
        (x2, y2) = (round(r*math.sin(p2_angle)) + offset_x, round(r*math.cos(p2_angle)) + offset_y)
        triangle = Triangle(x0, y0, x1, y1, x2, y2, fill=self.BLUE, outline=self.WHITE)
        circle = Circle(offset_x, offset_y, r, fill=None, outline=self.GREEN)
        self.append(circle)
        self.append(triangle)

    def set_icon(self):
        icon = displayio.OnDiskBitmap('images/video-card-32.bmp')
        icon_tg = displayio.TileGrid(icon, pixel_shader=icon.pixel_shader)
        icon_tg.x = 32
        icon_tg.y = 32
        self.append(icon_tg)

    # Show the GUI on the display
    def update(self, display):
        display.show(self)


# A Widget has a name, (x, y) location (upper left corner),
# and a (w, h) size in pixels.
# I'm going to start exploring layouts with 32px increments
class Widget():

    _active = False
    (_x, _y) = (0, 0)
    (_w, _h) = (0, 0)

    def __init__(self):
        self._active = True
        (_x, _y) = (0, 0)
        (_w, _h) = (32, 32)
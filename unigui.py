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

class Solarized():
    # palette = displayio.Palette()
    BASE03     = 0x002B36
    BASE3      = 0xFDF6E3
    YELLOW  = 0xB58900
    ORANGE  = 0xCB4B16
    RED     = 0xDC322F
    MAGENTA = 0xD33682
    VIOLET  = 0x6C71C4
    BLUE    = 0x268BD2
    CYAN    = 0x2AA198
    GREEN   = 0x859900


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
        self._x            = 0
        self._y            = 0
        self._width        = width
        self._height       = height
        self._bg_color     = Solarized.BASE03
        self._text_color   = Solarized.BASE3
        self._widgets      = []
        self._border_color = Solarized.VIOLET
        self._border       = False
        self._frame        = None
        super().__init__(scale=scale_factor)

    # Draws a triangle centered in the GUI
    def set_main_area(self):
        r = 200
        (offset_x, offset_y) = (round(self._width/2), round(self._height/2))
        # Get three random angles around our circle:
        p0_angle = math.radians(randint(0, 360))
        p1_angle = math.radians(randint(0, 360))
        p2_angle = math.radians(randint(0, 360))
        (x0, y0) = (round(r*math.sin(p0_angle)) + offset_x, round(r*math.cos(p0_angle)) + offset_y)
        (x1, y1) = (round(r*math.sin(p1_angle)) + offset_x, round(r*math.cos(p1_angle)) + offset_y)
        (x2, y2) = (round(r*math.sin(p2_angle)) + offset_x, round(r*math.cos(p2_angle)) + offset_y)
        triangle = Triangle(x0, y0, x1, y1, x2, y2, fill=Solarized.BLUE, outline=Solarized.YELLOW)
        circle = Circle(offset_x, offset_y, r, fill=None, outline=Solarized.CYAN)
        self.append(circle)
        self.append(triangle)

    def set_icon(self):
        icon = displayio.OnDiskBitmap('images/256x32/color_blocks.bmp')
        # icon_tg = displayio.TileGrid(icon, pixel_shader=icon.pixel_shader, width=1, height=1, tile_width=32, tile_height=32)
        for i in range(6):
            icon_tg = displayio.TileGrid(icon, pixel_shader=icon.pixel_shader, width=1, height=1, tile_width=32, tile_height=32)
            icon_tg[0] = randint(0, 5)
            icon_tg.x = 32*i
            icon_tg.y = 32
            self.append(icon_tg)

    def set_border(self, is_on):
        self._border = is_on
        if is_on:
            frame = Rect(self._x, self._y, self._width, self._height, fill=self._bg_color, outline=self._border_color)
            self._frame = frame
            self.append(self._frame)
        else:
            try:
                self.remove(self._frame)
            except:
                print("couldn't remove frame from UniGui!")

    def add_widget(self, widget):
        # TODO: first validate the layout
        self._widgets.append(widget)
        self.append(widget)

    # returns the Widget named <name>, or None
    def get_widget(self, name):
        match = None
        for widget in self._widgets:
            if widget._name == name:
                match = widget
        return match

    # This method makes sure that the widgets don't overlap
    def validate_layout(self):
        for widget in _widgets:
            pass  #TODO
            

    # Show the GUI on the display
    def update(self, display):
        display.show(self)



# A Widget has a name, (x, y) location (upper left corner),
# and a (w, h) size in pixels.
# I'm going to start exploring layouts with 32px increments
#  A Widget is a displayio.Group, but it also can be attached to events and be updated
class Widget(displayio.Group):

    def __init__(self, name, x, y, width, height):
        self._name         = name
        self._x            = x
        self._y            = y
        self._width        = width
        self._height       = height
        self._bg_color     = 0x000000
        self._border_color = 0xFF0000
        self._border       = False
        self._frame        = None
        super().__init__()
        # (self._region._x, self._region._y) = (0, 0)
        # (self._region._w, self._region._h) = (32, 32)

    def is_active(self):
        return self._active

    def set_bg(self, color):
        self._bg_color = color

    def set_border(self, is_on):
        self._border = is_on
        if is_on:
            frame = Rect(self._x, self._y, self._width, self._height, fill=None, outline=self._border_color)
            self._frame = frame
            self.append(self._frame)
        else:
            try:
                self.remove(self._frame)
            except:
                print("couldn't remove frame from Widget!")


# A Widget that displays a string nicely
class TextWidget(Widget):

    SMALL_FONT = "fonts/VCROSDMono-14.bdf"
    LARGE_FONT = "fonts/SNES-Italic-24.bdf"
                 #"fonts/Silom-Bold-24.bdf"

    def __init__(self, name, x, y, width, height, font_size=LARGE_FONT):
        super().__init__(name, x, y, width, height)
        self._value     = ""
        self._color     = Solarized.BASE3
        self._font_file = font_size
        font = bitmap_font.load_font(self._font_file)
        text_area = label.Label(font, text=self._value, color=self._color)
        # setup some properties
        text_area.base_alignment = True
        text_area.anchor_point = (0, 0)
        bb = text_area._bounding_box
        (w, h) = (bb[2] - bb[0], bb[3] - bb[1])
        (x, y) = (round(self._width/2) - round(w/2), self._y)
        text_area.anchored_position = (x, y)
        # frame = Rect(x, y, w, h, fill=self.BLACK, outline=self.DARK_GRAY)
        self._label = text_area ## Does this take up more memory?
        self.append(text_area)

    # sets the text to display
    def set_value(self, value):
        self._value = value
        self._label.text = value

    # sets the text color
    def set_color(self, color):
        self._color = color
        self._label.color = color


class Region():
    
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def get_start(self):
        return (self._x, self._y)
    
    def get_end(self):
        return (self._x + self._w, self._y + self._h)

    def get_width(self):
        return self._w

    def get_height(self):
        return self._h


# A TouchScreen is an object that can be clicked by something (a finger, a mouse pointer)
class TouchScreen():

    def __init__(self):
        self._active = True
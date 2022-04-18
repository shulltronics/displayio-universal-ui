import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
import math
from random import randint

class CustomColors():
    WHITE      = 0xFFFFFF
    BLACK      = 0x000000
    LIGHT_GRAY = 0x707070
    DARK_GRAY  = 0x454545
    RED        = 0xFF0000
    GREEN      = 0x00FF00
    BLUE       = 0x0000FF
    MAGENTA    = 0xFF00FF

class Solarized():
    
    BASE03  = 0x002B36
    BASE02  = 0x073642
    BASE01  = 0x586E75
    BASE00  = 0x657B83
    BASE0   = 0x839496
    BASE1   = 0x93A1A1
    BASE2   = 0xEEE8D5
    BASE3   = 0xFDF6E3
    YELLOW  = 0xB58900
    ORANGE  = 0xCB4B16
    RED     = 0xDC322F
    MAGENTA = 0xD33682
    VIOLET  = 0x6C71C4
    BLUE    = 0x268BD2
    CYAN    = 0x2AA198
    GREEN   = 0x859900
    light    = displayio.Palette(8)
    light[0] = BASE3    # Background
    light[1] = BASE2    # Background highlights
    light[2] = BASE00   # Default text
    light[3] = BASE01   # Emphasized text
    light[4] = BLUE     # Highlight 1
    light[5] = CYAN     # Highlight 2
    light[6] = MAGENTA  # Highlight 3
    light[7] = RED      # Highlight 4
    dark     = displayio.Palette(8)
    dark[0]  = BASE03   # Background
    dark[1]  = BASE02   # Background highlights
    dark[2]  = BASE0    # Default text
    dark[3]  = BASE1    # Emphasized text
    dark[4]  = BLUE
    dark[5]  = CYAN
    dark[6]  = MAGENTA
    dark[7]  = RED

"""
A Widget has a name, (x, y) location (upper left corner),
and a (w, h) size in pixels.
 A Widget is a displayio.Group, but it also can be attached to events and be updated
"""
class Widget(displayio.Group):

    def __init__(self, name, x, y, width, height):
        super().__init__()
        self.name          = name
        self.palette       = Solarized.dark
        self.x             = x
        self.y             = y
        self.width         = width
        self.height        = height
        self.border        = False
        self.background_bm = None   # this is the background bitmap
        self.background_tg = None
        self.clickable     = True   # by default a widget doesn't do anything when clicked
        self.callback      = self.border_toggle
        self.set_background()

    def set_background(self, bg_color_index=None):
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

    def border_on(self, color_idx=4):
        self.border = True
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
        self.border = False
        bm = self.background_bm
        # get the index of the background tilegrid.
        # Don't care about the tg itself because we're making a new one
        (tg_index, _) = self.get_background_tilegrid()
        bm.fill(0)
        self.background_tg = displayio.TileGrid(bm, pixel_shader=self.palette)
        self.insert(tg_index, self.background_tg)

    def border_toggle(self):
        if self.border:
            self.border_off()
        else:
            self.border_on()

    # Set the function to call when the widget is clicked
    def set_click_action(self, function):
        self.callback = function

"""
A Widget that displays a string nicely
"""
class TextWidget(Widget):

    SMALL_FONT = "fonts/6x12.bdf"
                 #"fonts/VCROSDMono-14.bdf"
    LARGE_FONT = "fonts/fipps-12pt.bdf"
                 #"fonts/SNES-Italic-24.bdf"
                 #"fonts/Silom-Bold-24.bdf"

    def __init__(self, name, x, y, width, height, font_size=LARGE_FONT):
        super().__init__(name, x, y, width, height)
        self.value     = "default"
        self.font_file = font_size
        self.color     = Solarized.YELLOW
        font = bitmap_font.load_font(self.font_file)
        text = label.Label(font, text=self.value, background=self.palette[1], color=self.color)
        # setup some properties
        text.base_alignment = True
        text.anchor_point = (0, 0)
        bb = text._bounding_box
        (w, h) = (bb[2] - bb[0], bb[3] - bb[1])
        (x, y) = (round(self.width/2) - round(w/2), self.y)
        text.anchored_position = (x, y)
        self.label = text ## Does this take up more memory?
        self.append(self.label)

    def get_label(self):
        try:
            idx = self.index(self.label)
            return (idx, self.pop(idx))
        except:
            print("Tried to get non-existant text label!")
            return None

    # sets the text to display
    def set_value(self, value):
        (label_idx, label) = self.get_label()
        if label:
            self.value = value
            label.text = self.value
            self.insert(label_idx, label)

    # sets the text color
    def set_color(self, color):
        self.color = color
        self.label.color = color


"""
This widget draws some graphics
"""
class GraphicsWidget(Widget):

    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.graphics = None

    def get_graphics_group(self):
        try:
            idx = self.index(self.graphics)
            return (idx, self.pop(idx))
        except:
            print("Tried to get non-existant graphics group!")
            return None

    # Draws a random triangle centered in the widget
    def set_main_area(self):
        (offset_x, offset_y) = (round(self.width/2), round(self.height/2))
        r = min(offset_x, offset_y)
        # Get three random angles around our circle:
        p0_angle = math.radians(randint(0, 360))
        p1_angle = math.radians(randint(0, 360))
        p2_angle = math.radians(randint(0, 360))
        (x0, y0) = (round(r*math.sin(p0_angle)) + offset_x, round(r*math.cos(p0_angle)) + offset_y)
        (x1, y1) = (round(r*math.sin(p1_angle)) + offset_x, round(r*math.cos(p1_angle)) + offset_y)
        (x2, y2) = (round(r*math.sin(p2_angle)) + offset_x, round(r*math.cos(p2_angle)) + offset_y)
        triangle = Triangle(x0, y0, x1, y1, x2, y2, fill=self.palette[5], outline=self.palette[6])
        # if the graphics already exist, update them
        if self.graphics:
            (graphics_idx, graphics) = self.get_graphics_group()
            self.graphics = triangle
            self.insert(graphics_idx, self.graphics)
        else:
            self.graphics = triangle
            self.append(self.graphics)
        # circle = Circle(offset_x, offset_y, r, fill=None, outline=self.palette[7])
        # self.graphics.append(circle)
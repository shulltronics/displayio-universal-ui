from unigui.colorscheme import *
import displayio
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.circle import Circle
import math
from random import randint
from pkg_resources import resource_filename

class Widget(displayio.Group):
    """
    A Widget has a name, (x, y) location (upper left corner),
    and a (w, h) size in pixels.
    A Widget is a displayio.Group, and thus has the following properties:
    - It can have a list of children
    - etc..
    It also has the following properties:
    - it can be attached to events and be updated
    - it will adopt the GUI's colorshceme unless an overide colorscheme is passed as an argument
    """
    def __init__(self, name, x, y, width, height, colorscheme, scale=1):
        super().__init__(scale=scale)
        self.name          = name
        self.palette       = colorscheme
        self.palette.make_transparent(0)
        self.bg_transparent = False
        self.x             = x
        self.y             = y
        self.width         = width
        self.height        = height
        self.border        = False
        self.background_bm = None
        self.background_tg = None
        # by default a widget doesn't do anything when clicked
        self.clickable     = False
        # the callback function should take the click location tuple (xpos, ypos) as an argument
        self.callback      = None
        self.set_background()

    def get_background_tilegrid(self):
        """
        Return the tuple (index, TileGrid) that represents the widget's background.
        If the TileGrid already exists in the widget, it pops and returns that one,
        otherwise it creates and returns it without appending it to the group.
        """
        try:
            idx = self.index(self.background_tg)
            return (idx, self.pop(idx))
        except:
            print("Creating background tilegrid...")
            bg_bitmap = displayio.Bitmap(self.width, self.height, 8)
            self.background_bm = bg_bitmap
            self.background_tg = displayio.TileGrid(bg_bitmap, pixel_shader=self.palette)
            return (0, self.background_tg)

    def set_bg_transparent(self, trans):
        """ Sets the transparency of the widget's background (True or False). """
        self.bg_transparent = trans
        self.set_background()

    def set_background(self, bg_color_index=ColorScheme.indices['BASE']):
        """
        Set the background to the specified colorscheme index.
        """
        (tg_idx, tg) = self.get_background_tilegrid()   # Get the bg TileGrid
        if self.bg_transparent:
            self.background_bm.fill(0)
        else:
            self.background_bm.fill(bg_color_index)
        new_tg = displayio.TileGrid(self.background_bm, pixel_shader=self.palette)
        self.background_tg = new_tg
        self.insert(tg_idx, self.background_tg)

    def border_on(self, color_idx=ColorScheme.indices['BASE_HIGHLIGHT']):
        """
        Draw a 1px wide border around the widget.
        """
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
        """
        Clear the border around the widget.
        """
        self.border = False
        bm = self.background_bm
        # get the index of the background tilegrid.
        # Don't care about the tg itself because we're making a new one
        (tg_index, _) = self.get_background_tilegrid()
        # Fill with the base color index
        bm.fill(ColorScheme.indices['BASE'])
        self.background_tg = displayio.TileGrid(bm, pixel_shader=self.palette)
        self.insert(tg_index, self.background_tg)

    def border_toggle(self, click_pos):
        if self.border:
            self.border_off()
        else:
            self.border_on()

    # Set the function to call when the widget is clicked
    def set_click_action(self, function):
        self.clickable = True
        self.callback = function

class TextWidget(Widget):
    """
    A Widget that displays a string nicely
        TODO: Add padding 
        TODO: ability to wrap, cutoff, or scroll long text
    """
    SMALL_FONT = resource_filename('unigui', 'fonts/6x12.bdf')
                 #"fonts/VCROSDMono-14.bdf"
    LARGE_FONT = resource_filename('unigui', 'fonts/fipps-12pt.bdf')
                 #"fonts/SNES-Italic-24.bdf"
                 #"fonts/Silom-Bold-24.bdf"

    def __init__(self, name, x, y, width, height, colorscheme, font_path=None):
        super().__init__(name, x, y, width, height, colorscheme)
        self.value = ""
        if font_path:
            self.font = bitmap_font.load_font(font_path)
        else:
            self.font = terminalio.FONT
        self.color = self.palette[ColorScheme.indices['TEXT']]
        self.label = label.Label(self.font, text=self.value, background=None, color=self.color)
        self.append(self.label)

    def get_label(self):
        try:
            idx = self.index(self.label)
            return (idx, self.pop(idx))
        except:
            print("Tried to get non-existant text label!")
            return None

    def set_value(self, value, h_justification='center', v_justification='center'):
        """
        Set the text that the widget should display.
        """
        if self.value == value:
            return
        (label_idx, label) = self.get_label()
        if label:
            self.value = value
            # Set the text value and then recalculate its position
            label.text = self.value
            label.anchor_point = (0, 0)
            bb = label._bounding_box
            (w, h) = (bb[2] - bb[0], bb[3] - bb[1])
            #TODO make this an object parameter
            x_padding = y_padding = 3

            if v_justification == 'top':
                y = y_padding
            elif v_justification == 'center':
                y = round(self.height/2) - round(h/2)
            elif v_justification == 'bottom':
                y = self.height - h
            
            if h_justification == 'left':
                x = x_padding
            elif h_justification == 'center':
                x = round(self.width/2) - round(w/2)
            elif h_justification == 'right':
                x = self.width - w - x_padding
            
            label.anchored_position = (x, y)
            self.insert(label_idx, label)

    # sets the text color
    def set_color(self, color_idx=ColorScheme.indices['TEXT']):
        """
        Set the text color using an index into the colorscheme
        """
        self.color = self.palette[color_idx]
        self.label.color = self.color

class IconWidget(Widget):

    ICON_BUILTIN = resource_filename('unigui', 'images/128x32/px_icons.bmp')

    def __init__(self, name, x, y, width, height, colorscheme):
        self.icon_path = self.ICON_BUILTIN
        self.bm, self.icon_palette = adafruit_imageload.load(
            self.icon_path,
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        # print("icon palette length is ", self.icon_palette.__len__())
        super().__init__(name, x, y, width, height, colorscheme=colorscheme)
        # Setup the icon palette to the color we want, making index 0 transparent
        # Be sure when creating icons to make the background color be index 0
        self.icon_palette.make_transparent(0)
        self.icon_palette[1] = self.palette[ColorScheme.indices['COLOR_2']]
        self.tg = displayio.TileGrid(
            self.bm,
            pixel_shader=self.icon_palette,
            width=1,
            height=1,
            tile_width=32,
            tile_height=32,
            default_tile=2,
        )
        self.append(self.tg)

    def set_icon_index(self, idx=0):
        self.tg[0] = idx

class GraphicsWidget(Widget):
    """
    This widget draws some graphics
    """
    def __init__(self, name, x, y, width, height, colorscheme):
        super().__init__(name, x, y, width, height, colorscheme)
        self.graphics = None

    def get_graphics_group(self):
        try:
            idx = self.index(self.graphics)
            return (idx, self.pop(idx))
        except:
            print("Tried to get non-existant graphics group!")
            return None

    # Draws a random triangle centered in the widget
    def set_main_area(self, click_pos):
        (offset_x, offset_y) = (round(self.width/2), round(self.height/2))
        padding = 10 # TODO: paramatrize this value
        r = min(offset_x, offset_y) - padding
        # Get three random angles around our circle:
        p0_angle = math.radians(randint(0, 360))
        p1_angle = math.radians(randint(0, 360))
        p2_angle = math.radians(randint(0, 360))
        (x0, y0) = (round(r*math.sin(p0_angle)) + offset_x, round(r*math.cos(p0_angle)) + offset_y)
        (x1, y1) = (round(r*math.sin(p1_angle)) + offset_x, round(r*math.cos(p1_angle)) + offset_y)
        (x2, y2) = (round(r*math.sin(p2_angle)) + offset_x, round(r*math.cos(p2_angle)) + offset_y)
        triangle = Triangle(x0, y0, x1, y1, x2, y2,
            fill=self.palette[ColorScheme.indices['COLOR_0']],
            outline=self.palette[ColorScheme.indices['COLOR_1']],
        )
        # if the graphics already exist, update them
        if self.graphics:
            (graphics_idx, graphics) = self.get_graphics_group()
            self.graphics = triangle
            self.insert(graphics_idx, self.graphics)
        else:
            self.graphics = triangle
            self.append(self.graphics)

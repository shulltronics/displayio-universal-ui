import displayio

"""
A ColorScheme is a palette of size 8
"""
class ColorScheme():
    indices = {
        'TRANSPARENT':    0,
        'BASE':           1,
        'BASE_HIGHLIGHT': 2,
        'TEXT':           3,
        'TEXT_HIGHLIGHT': 4,
        'COLOR_0':        5,
        'COLOR_1':        6,
        'COLOR_2':        7,
    }


class Shulltronics(ColorScheme):
    WHITE      = 0xFFFFFF
    BLACK      = 0x000000
    LIGHT_GRAY = 0x707070
    DARK_GRAY  = 0x454545
    RED        = 0xFF0000
    GREEN      = 0x00FF00
    BLUE       = 0x0000FF
    MAGENTA    = 0xFF00FF

    dark = displayio.Palette(8)
    dark[ColorScheme.indices['TRANSPARENT']]    = 0          # Transparent
    dark[ColorScheme.indices['BASE']]           = BLACK      # Background
    dark[ColorScheme.indices['BASE_HIGHLIGHT']] = DARK_GRAY  # Background highlights
    dark[ColorScheme.indices['TEXT']]           = LIGHT_GRAY # Default text
    dark[ColorScheme.indices['TEXT_HIGHLIGHT']] = WHITE      # Emphasized text
    dark[ColorScheme.indices['COLOR_0']]        = BLUE
    dark[ColorScheme.indices['COLOR_1']]        = RED
    dark[ColorScheme.indices['COLOR_2']]        = MAGENTA


class Solarized(ColorScheme):
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

    light = displayio.Palette(8)
    light[ColorScheme.indices['TRANSPARENT']]    = 0        # Transparent
    light[ColorScheme.indices['BASE']]           = BASE3    # Background
    light[ColorScheme.indices['BASE_HIGHLIGHT']] = BASE03   # Background highlights
    light[ColorScheme.indices['TEXT']]           = BASE00   # Default text
    light[ColorScheme.indices['TEXT_HIGHLIGHT']] = BASE01   # Emphasized text
    light[ColorScheme.indices['COLOR_0']]        = BLUE     # Highlight 1
    light[ColorScheme.indices['COLOR_1']]        = CYAN     # Highlight 2
    light[ColorScheme.indices['COLOR_2']]        = MAGENTA  # Highlight 3
    
    dark = displayio.Palette(8)
    dark[ColorScheme.indices['TRANSPARENT']]    = 0
    dark[ColorScheme.indices['BASE']]           = BASE03
    dark[ColorScheme.indices['BASE_HIGHLIGHT']] = BASE02
    dark[ColorScheme.indices['TEXT']]           = BASE2
    dark[ColorScheme.indices['TEXT_HIGHLIGHT']] = BASE3
    dark[ColorScheme.indices['COLOR_0']]        = BLUE
    dark[ColorScheme.indices['COLOR_1']]        = GREEN
    dark[ColorScheme.indices['COLOR_2']]        = RED


class VSCode():
    BASE03  = 0x000000
    BASE02  = 0x202020
    BASE01  = 0x586E75
    BASE00  = 0x657B83
    BASE0   = 0x839496
    BASE1   = 0x93A1A1
    BASE2   = 0xEEE8D5
    BASE3   = 0xFDF6E3
    YELLOW  = 0xB58900
    ORANGE  = 0xF38518
    RED     = 0xFF0000
    MAGENTA = 0xD33682
    VIOLET  = 0xB267E6
    BLUE    = 0x6796E6
    CYAN    = 0x9CDCFE
    GREEN   = 0x008000

    light = displayio.Palette(8)
    light[ColorScheme.indices['TRANSPARENT']]    = 0x010101        # Transparent
    light[ColorScheme.indices['BASE']]           = BASE3    # Background
    light[ColorScheme.indices['BASE_HIGHLIGHT']] = BASE03    # Background highlights
    light[ColorScheme.indices['TEXT']]           = ORANGE   # Default text
    light[ColorScheme.indices['TEXT_HIGHLIGHT']] = BASE01   # Emphasized text
    light[ColorScheme.indices['COLOR_0']]        = BLUE     # Highlight 1
    light[ColorScheme.indices['COLOR_1']]        = CYAN     # Highlight 2
    light[ColorScheme.indices['COLOR_2']]        = MAGENTA  # Highlight 3
    
    dark = displayio.Palette(8)
    dark[ColorScheme.indices['TRANSPARENT']]    = 0x010101
    dark[ColorScheme.indices['BASE']]           = BASE03
    dark[ColorScheme.indices['BASE_HIGHLIGHT']] = BASE02
    dark[ColorScheme.indices['TEXT']]           = ORANGE
    dark[ColorScheme.indices['TEXT_HIGHLIGHT']] = BASE03
    dark[ColorScheme.indices['COLOR_0']]        = BLUE
    dark[ColorScheme.indices['COLOR_1']]        = GREEN
    dark[ColorScheme.indices['COLOR_2']]        = ORANGE

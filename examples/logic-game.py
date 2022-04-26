from context import unigui

from unigui.unigui import UniGui
from unigui.widget import TextWidget, Widget
from unigui.pygame_display import PygameDisplay
import time
from random import randint


# This class creates a visual representation of an 8 bit register
class RegisterWidget(Widget):

    def __init__(self, number):
        super().__init__("register", 32, 0, 256, 32)
        self.border_on(6)
        # TODO - make click distinguishable between left and right "buttons"
        self.clickable = True
        self.callback = self.process_click
        self.number = number
        # initialize the bits
        self.bits = []
        for bit in range(8):
            xpos = 224 - 32*bit
            bit_widget = Widget(str(bit), xpos, 0, 32, 32)
            # If the bit is set, color in the block with a bright color
            # otherwise make it transparent
            if self.number & (1 << bit):
                bit_widget.set_background(5)
            else:
                bit_widget.set_background(1)
            bit_widget.border_on(6)
            # Add the bit to our local list and to the Group
            self.bits.append(bit_widget)
            self.append(bit_widget)
        # Setup the buttons to allow left and right clicking
        self.setup_buttons()

    # update the graphics to reflect self.number
    def update_bits(self):
        for (i, _bit) in enumerate(self.bits):
            # get the bit's index, and then get the bit
            try:
                bit_idx = self.index(_bit)
            except:
                print("RegisterWidget error: couldn't find bit!")
            bit = self.pop(bit_idx)
            # now updated it's background according to the new number
            if self.number & (1 << i):
                bit.set_background(5)
            else:
                bit.set_background(1)
            bit.border_on(6)
            # now put the bit back
            self.insert(bit_idx, bit)

    def setup_buttons(self):
        self.left_button  = Widget("button_left", self.x, self.y, round(self.width/2), self.height)
        self.left_button.clickable = True
        self.right_button = Widget("button_right", round(self.width/2), self.y, round(self.width/2), self.height)
        self.right_button.clickable = True
        self.left_button.callback  = self.decrement
        self.right_button.callback = self.increment
        self.append(self.left_button)
        self.append(self.right_button)

    def process_click(self, click_pos):
        (x, y) = click_pos
        print("relative click pos: " + str(click_pos))
        for button in [self.left_button, self.right_button]:
            x_min = button.x
            x_max = button.x + button.width
            y_min = button.y
            y_max = button.y + button.height
            contains_x = (x >= x_min) and (x < x_max)
            contains_y = (y >= y_min) and (y < y_max)
            if contains_x and contains_y:
                print("clicked button: " + str(button.name))
                button.callback()

    def decrement(self):
        if self.number > 0:
            self.number -= 1
        else:
            self.number = 255
        self.update_bits()

    def increment(self):
        if self.number < 255:
            self.number += 1
        else:
            self.number = 0
        self.update_bits()

# Configuration constants
WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale=SCALE_FACTOR)

# create our title area:
title = TextWidget("toolbar", 0, HEIGHT-32, round(WIDTH/2), 32)
title.set_value("Logic Puzzle Minigame", h_justification="left")
gui.add_widget(title)

# create a seconds counter:
timer = TextWidget("timer", round(WIDTH/2), HEIGHT-32, round(WIDTH/2), 32)
timer.set_value("0", h_justification="right")
gui.add_widget(timer)

# Setup a list of 8 bit registers
registers = []
for i in range(3):
    register = RegisterWidget(randint(0, 256))
    register.x = 32
    register.y = 32*i
    registers.append(register)
    gui.add_widget(register)

display = PygameDisplay(WIDTH*SCALE_FACTOR, HEIGHT*SCALE_FACTOR)
gui.update(display)

start_time = time.time()
while True:
    display.refresh()
    click = display.get_mouse_clicks()
    if click is not None:
        print(gui.__len__())
        print("click: " + str(click))
        gui.process_click(click)

    # Go through the numbers and see if any two adjacent ones match
    # if so, you've won the game, and we quit
    for i in range(len(registers)):
        if i is len(registers)-1:
            break
        if registers[i].number == registers[i+1].number:
            display.quit()

    # update the timer
    dt = round(time.time() - start_time)
    timer.set_value(str(dt), h_justification="right")

    time.sleep(0.1)
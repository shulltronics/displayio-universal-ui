from context import unigui
import displayio
from unigui.unigui import UniGui
from unigui.widget import GraphicsWidget, TextWidget, Widget
from adafruit_display_shapes.line import Line
from unigui.pygame_display import PygameDisplay
import time
import math
from random import randint

# A Branch has an angle relative to its parent (in degrees)
# and a length
class Branch():
    BASE_LEN = 10
    DEF_ANGLE = 40
    def __init__(self, angle, length):
        # Children should be branches too
        self.left  = None
        self.left_divisor = 1.2 + (randint(50, 100) / 100)
        self.right_divisor = 1.2 + (randint(50, 100) / 100)
        self.right = None
        self.generation = 0
        self.length = length
        self.angle = angle
        # self.grow(generations-1)

    # Grow n number of nodes on the tree
    def grow(self, n):
        if n == 0:
            return
        if n == 1:
            # Just append a new branch
            self.left = Branch(-self.DEF_ANGLE, self.length/self.left_divisor)
            self.left.generation = self.generation + 1
            self.right = Branch(self.DEF_ANGLE, self.length/self.right_divisor)
            self.right.generation = self.generation + 1
        else:
            # Append a new branch and then grow the rest
            self.left = Branch(-self.DEF_ANGLE, self.length/self.left_divisor)
            self.left.generation = self.generation + 1
            self.right = Branch(self.DEF_ANGLE, self.length/self.right_divisor)
            self.right.generation = self.generation + 1
            self.left.grow(n-1)
            self.right.grow(n-1)

    def print(self):
        print("gen: " + str(self.generation) + ", angle: " + str(self.angle) + ", len: " + str(self.length))
        if self.left is not None:
            self.left.print()
        if self.right is not None:
            self.right.print()

    # This method returns a Group with lines representing the branches of the tree
    def draw(self, start_position, acc_angle=0):
        gfx = displayio.Group()
        (x0, y0) = start_position
        acc_angle += self.angle
        # Get the end position using the angle and length
        x1 = x0 + self.length*math.sin(math.radians(acc_angle))
        x1 = round(x1)
        y1 = y0 - self.length*math.cos(math.radians(acc_angle))
        y1 = round(y1)
        g = self.generation % 3
        if g == 0:
            c = 0xFF0000
        elif g == 1:
            c = 0xFFFF00
        elif g == 2:
            c = 0xFFFFFF
        line = Line(x0, y0, x1, y1, color=c)
        gfx.append(line)
        if self.left is not None:
            gfx.append(self.left.draw((x1, y1), acc_angle=acc_angle))
        if self.right is not None:
            gfx.append(self.right.draw((x1, y1), acc_angle=acc_angle))
        return gfx


class TreeWidget(Widget):

    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.gfx = None
        self.regrow()

    def regrow(self):
        div = 2 + (randint(0, 100) / 100)
        self.tree = Branch(0, round(self.height/div))
        self.tree.grow(6)

    def click_action(self, click_pos):
        self.regrow()
        self.set_main_area()

    def set_main_area(self):
        # first try to get the graphics layer if it exists
        try:
            gfx_idx = self.index(self.gfx)
            self.pop(gfx_idx)
        except:
            print("oops!")
        start_pos = (round(self.width/2), self.height)
        self.gfx = self.tree.draw(start_pos)
        print("length: " + str(self.__len__()))
        self.append(self.gfx)
        
        
            

# Configuration constants
WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale=SCALE_FACTOR)

# create our title area:
title = TextWidget("toolbar", 0, HEIGHT-32, round(WIDTH/2), 32)
title.set_value("Tree Growth Simulation", h_justification="left")
gui.add_widget(title)

# create a seconds counter:
timer = TextWidget("timer", round(WIDTH/2), HEIGHT-32, round(WIDTH/2), 32)
timer.set_value("0", h_justification="right")
gui.add_widget(timer)

# Create the main simulation window
tree = TreeWidget("tree", 0, 0, WIDTH, HEIGHT-32)
tree.set_click_action(tree.click_action)
gui.add_widget(tree)

# Create the display and update it
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

    # update the timer
    dt = round(time.time() - start_time)
    timer.set_value(str(dt), h_justification="right")

    time.sleep(0.1)
from context import unigui

from unigui.unigui import UniGui
from unigui.widget import GraphicsWidget, TextWidget, Widget
from adafruit_display_shapes.line import Line
from unigui.pygame_display import PygameDisplay
import time
from random import randint

# A Branch has an angle relative to its parent (in degrees)
# and a length
class Branch():
    BASE_LEN = 10
    def __init__(self, angle, length, generations):
        # Children should be branches too
        self.children = []
        self.generation = 0
        self.length = length
        self.angle = angle
        self.grow(generations-1)

    # Grow n number of nodes on the tree
    def grow(self, n):
        if n == 0:
            return
        if n == 1:
            # left_branch = Branch(10, BASE_LEN)
            right_branch = Branch(10, Branch.BASE_LEN, n)
            self.children.append(right_branch)
        else:
            right_branch = Branch(10, Branch.BASE_LEN + n, n)
            right_branch.generation = n
            self.children.append(right_branch)
            for child in self.children:
                child.grow(n-1)

    def print(self):
        for child in self.children:
            child.print()
        print("gen: " + str(self.generation) + ", angle: " + str(self.angle) + ", len: " + str(self.length))

root = Branch(0, 100, 1)
root.print()

class TreeWidget(Widget):

    def __init__(self, name, x, y, width, height, tree):
        super().__init__(name, x, y, width, height)
        self.tree = tree

    def set_main_area(self, click_pos):
        (x, y) = (round(self.width/2), self.height)
        gfx = Line(x, y, x, y-self.tree.length, color=0x00FF00)
        self.append(gfx)
            

# Configuration constants
WIDTH = 320
HEIGHT = 240
SCALE_FACTOR = 2
# The main UniGui object
gui = UniGui(WIDTH, HEIGHT, scale=SCALE_FACTOR)

# create our title area:
title = TextWidget("toolbar", 0, HEIGHT-32, round(WIDTH/2), 32)
title.set_value(" Tree Growth Simulation", h_justification="left")
gui.add_widget(title)

# create a seconds counter:
timer = TextWidget("timer", round(WIDTH/2), HEIGHT-32, round(WIDTH/2), 32)
timer.set_value("0", h_justification="right")
gui.add_widget(timer)

# Create the main simulation window
tree = TreeWidget("tree", 0, 0, WIDTH, HEIGHT-32, root)
tree.set_click_action(tree.set_main_area)
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
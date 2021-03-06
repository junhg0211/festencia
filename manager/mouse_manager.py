from pygame import mouse
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.event import Event

from handler import Handler


class MouseManager(Handler):
    """ A class that handles mouse events. """

    def __init__(self):
        self.left = False
        self.right = False
        self.middle = False

        self.left_start = False
        self.middle_start = False
        self.right_start = False

        self.left_end = False
        self.middle_end = False
        self.right_end = False

        self.x, self.y = 0, 0

    def set_pos(self, x: float, y: float):
        """ Sets the mouse position in the window. """
        mouse.set_pos(x, y)
        self.x = x
        self.y = y

    def handle(self, event: Event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_start = True
                self.left = True
            elif event.button == 2:
                self.middle_start = True
                self.middle = True
            elif event.button == 3:
                self.right_start = True
                self.right = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.left_end = True
                self.left = False
            elif event.button == 2:
                self.middle_end = True
                self.middle = False
            elif event.button == 3:
                self.right_end = True
                self.right = False
        elif event.type == MOUSEMOTION:
            self.x, self.y = event.pos

    def tick(self):
        """ Resets the mouse button states. Called every tick's last part. """
        self.left_start = False
        self.left_end = False
        self.middle_start = False
        self.middle_end = False
        self.right_start = False
        self.right_end = False

from collections import Callable
from typing import Optional

from clipboard import paste
from pygame import draw

from display import Display
from manager import MouseManager, KeyboardManager
from object import Object
from util import Face, center


class Text(Object):
    def __init__(self, text: str, face: Face, x: int = 0, y: int = 0):
        super().__init__(x, y)

        self.text = text
        self.face = face

        self.surface = self.face.render(self.text)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def center(self, display: Display) -> 'Text':
        """ Centers the text on the display. """

        self.set_x(center(display.width, self.width))
        self.center_y(display)
        return self

    def center_x(self, display: Display) -> 'Text':
        self.set_x(center(display.width, self.width))
        return self

    def center_y(self, display: Display) -> 'Text':
        self.set_y(center(display.height, self.height))
        return self

    def set_font(self, font_path: str) -> 'Text':
        self.face.set_font(font_path)
        self.surface = self.face.render(self.text)
        return self

    def set_text(self, text: str) -> 'Text':
        self.surface = self.face.render(text)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        return self

    def render(self, display: Display):
        display.display.blit(self.surface, (self.x, self.y))


class TextButton(Text):
    """ A text object that can be clicked. """

    def __init__(self, text: str, face: Face, action: Callable, mouse_manager: MouseManager, x: int = 0, y: int = 0):
        super().__init__(text, face, x, y)

        self.action = action
        self.mouse_manager = mouse_manager

    def mouse_in(self):
        """ Returns True if the mouse is in the button. """
        return self.x < self.mouse_manager.x < self.x + self.width \
            and self.y < self.mouse_manager.y < self.y + self.height

    def tick(self):
        if self.mouse_manager.left_end:
            if self.mouse_in():
                self.action()


class TextInserter(TextButton):
    """ A text object that can be clicked and typed into. """

    def __init__(self, text_template: str, face: Face, mouse_manager: MouseManager,
                 keyboard_manager: KeyboardManager, default_text: str = '', ender: Optional[Callable] = None,
                 x: int = 0, y: int = 0):
        super().__init__(text_template.format(default_text), face, self.insert, mouse_manager, x, y)
        self.ender = ender

        self.text_template = text_template

        self.keyboard_manager = keyboard_manager

        self.inserting = False
        self.inserted = default_text

    def insert(self):
        self.inserting = True
        self.keyboard_manager.pop()

    def set_inserted(self, inserted):
        self.inserted = inserted
        self.set_text(self.text_template.format(self.inserted))

    def tick(self):
        super().tick()

        if self.inserting:
            inserting_off = False
            self.inserted += self.keyboard_manager.pop()
            if self.inserted:
                if self.inserted[-1] == '\b':
                    self.inserted = self.inserted[:-2]
                elif self.inserted[-1] == '\r':
                    self.inserted = self.inserted[:-1]
                    inserting_off = True
                elif self.inserted[-1] == '\x16':
                    self.inserted = self.inserted[:-1] + paste()
                elif self.inserted[-1] in '\x7f':
                    self.inserted = ''
                elif self.inserted[-1] in ('\t', '\n', '\x1b'):
                    self.inserted = self.inserted[:-1]
            if self.mouse_manager.left_start and not self.mouse_in() \
                    or inserting_off:
                self.inserting = False
                if self.ender is not None:
                    self.ender()
            self.set_text(self.text_template.format(self.inserted))

    def render(self, display: Display):
        super().render(display)
        if self.inserting:
            draw.line(display.display, self.face.color,
                      (self.x, self.y + self.height), (self.x + self.width, self.y + self.height))

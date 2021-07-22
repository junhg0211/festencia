from pygame.constants import KEYDOWN, KEYUP
from pygame.event import Event

from handler import Handler


class KeyboardManager(Handler):
    def __init__(self):
        self.pressed = set()
        self.down = set()
        self.up = set()

        self.buffer = ''

    def pop(self) -> str:
        buffer = self.buffer
        self.buffer = ''
        return buffer

    def handle(self, event: Event):
        self.down.clear()
        self.up.clear()

        if event.type == KEYDOWN:
            self.pressed.add(event.key)
            self.up.add(event.key)
            self.buffer += event.unicode
        elif event.type == KEYUP:
            self.pressed -= {event.key}
            self.down.add(event.key)

    def is_pressed(self, key: int):
        return key in self.pressed

    def is_down(self, key: int):
        return key in self.down

    def is_up(self, key: int):
        return key in self.up

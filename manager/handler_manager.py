from typing import List

from pygame.event import Event

from handler import Handler


class HandlerManager(Handler):
    def __init__(self):
        self.handlers: List[Handler] = list()

    def add(self, handler: Handler):
        self.handlers.append(handler)
        return self

    def handle(self, event: Event):
        for handler in self.handlers:
            handler.handle(event)

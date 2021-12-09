from pygame.constants import QUIT
from pygame.event import Event

from handler import Handler


class Quit(Handler):
    """ Handler for quit events. """

    def __init__(self, shutdown):
        self.shutdown = shutdown

    def handle(self, event: Event):
        if event.type == QUIT:
            self.shutdown()

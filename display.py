from pygame import display, FULLSCREEN
from pygame.surface import Surface


class Display:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height

        display.set_caption(title)

        # self.display: Surface = display.set_mode((3840, 2160), FULLSCREEN)
        self.display: Surface = display.set_mode((self.width, self.height))

    @staticmethod
    def flip():
        display.flip()

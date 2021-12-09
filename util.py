from datetime import datetime
from math import inf, pi

from pygame import Surface
from pygame.font import Font

radian = 180 / pi


def limit(value: float, m: float, x: float):
    return max(min(value, x), m)


def center(area: int or float, size: int or float) -> int:
    return (area - size) // 2


def get_friction(fps_, ratio: float = 1.7747e-05) -> float:
    try:
        return 1 / (1 - ratio ** (1 / fps_))
    except ZeroDivisionError:
        return inf


def animate(value: int, target: int, fps) -> int:
    delta = target - value
    value += delta / get_friction(fps)
    return value


def linear(value, min_, max_, from_, to):
    return (value - min_) / (max_ - min_) * (to - from_) + from_


class Face:
    """
    A class that represents a font face, used in Text class.
    """

    def __init__(self, font_path: str, font_size: int, color: tuple):
        self.path = font_path
        self.size = font_size
        self.color = color

        self.font = Font(self.path, self.size)

    def set_font(self, font_path: str):
        self.path = font_path
        self.font = Font(self.path, self.size)
        return self

    def render(self, text: str) -> Surface:
        return self.font.render(text, True, self.color)


class Spacer:
    """ A class that helps to create a space between multiple objects. """

    def __init__(self, gap: int, *objects):
        self.gap = gap
        self.objects = objects

    def get_width(self) -> int:
        """ Returns the width of the whole objects when they're spaced. """
        result = self.gap * (len(self.objects) - 1)
        for object_ in self.objects:
            result += object_.width
        return result

    def tick(self):
        dx = self.objects[0].x
        for i, object_ in enumerate(self.objects):
            if i:
                object_.set_x(dx)
            dx += object_.width + self.gap


class Log:
    """ A class that helps to log information."""

    @staticmethod
    def debug(message):
        print(f'{datetime.now()} [DEBUG] {message}')

    @staticmethod
    def server(message):
        print(f'{datetime.now()} [SERVER] {message}')

    @staticmethod
    def client(message):
        print(f'{datetime.now()} [CLIENT] {message}')

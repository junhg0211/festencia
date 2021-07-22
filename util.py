from math import inf

from pygame import Surface
from pygame.font import Font


def limit(value: float, m: float, x: float) -> float:
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


def interpolate(value, min_, max_, from_, to):
    return (value - min_) / (max_ - min_) * (to - from_) + from_


class Face:
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
    def __init__(self, gap: int, *objects):
        self.gap = gap
        self.objects = objects

    def get_width(self) -> int:
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
    @staticmethod
    def server(message):
        print(message)

import random
from math import hypot, sqrt
from typing import Optional

from pygame import gfxdraw, draw

from const import RED, GREEN, BLACK, BLUE
from display import Display
from object import Object, FPSCalculator
from util import animate


class Dualcircles(Object):
    @staticmethod
    def get_radius(display: Display) -> int:
        return (display.width + display.height) // 4

    def __init__(self, x: int, y: int, x2: int, y2: int, radius: int or Display,
                 fps_calculator: Optional[FPSCalculator] = None):
        super().__init__(x, y)
        self.x2 = x2
        self.y2 = y2
        if isinstance(radius, Display):
            self.radius = Dualcircles.get_radius(radius)
        else:
            self.radius = int(radius)
        self.fps_calculator = fps_calculator

        self.target_x = self.x
        self.target_x2 = self.x2
        self.target_y = self.y
        self.target_y2 = self.y2

        self.critical_line = False

        self.x_1 = 0
        self.x_2 = 0
        self.condition = False

    def random_pos(self, display: Display) -> 'Dualcircles':
        self.target_x = random.randint(0, display.width)
        self.target_x2 = random.randint(0, display.width)
        self.target_y = random.randint(0, display.height)
        self.target_y2 = random.randint(0, display.height)
        return self

    def tick(self):
        if self.fps_calculator:
            fps = self.fps_calculator.fps
        else:
            fps = 500
        self.x = animate(self.x, self.target_x, fps)
        self.x2 = animate(self.x2, self.target_x2, fps)
        self.y = animate(self.y, self.target_y, fps)
        self.y2 = animate(self.y2, self.target_y2, fps)

        self.critical_line = (distance := hypot(self.x - self.x2, self.y - self.y2)) <= self.radius

        self.condition = distance < self.radius and self.y != self.y2

        if self.condition:
            a = self.x
            b = self.x2
            c = self.y
            d = self.y2
            r = self.radius

            # a_ = (a**2-2*a*b+b**2+c**2+d**2-2*c*d)/(c-d)**2
            # b_ = (-a**3+a**2*b+a*b**2-a*c**2-a*d**2+2*a*c*d-b**3-b*c**2-b*d**2+2*b*c*d)/(c-d)**2
            # c_ = ((a**4+b**4+c**4+d**4)/4
            #       + (-a**2*b**2+a**2*c**2+a**2*d**2+b**2*c**2+b**2*d**2+3*c**2*d**2)/2
            #       + (-a**2*c*d-b**2*c*d-c**3*d-c*d**3))/(c-d)**2 - r**2
            a_ = a**2 - 2*a*b + b**2 + c**2 - 2*c*d + d**2
            b_ = -a**3 + a**2*b + a*b**2 - a*c**2 + 2*a*c*d - a*d**2 - b**3 - b*c**2 + 2*b*c*d - b*d**2
            d_ = -(c-d)**2 * a_ * (a_ - 4*r**2)

            self.x_1 = (-b_ + sqrt(d_)) / (2 * a_)
            self.x_2 = (-b_ - sqrt(d_)) / (2 * a_)

    # noinspection DuplicatedCode
    def render(self, display: Display):
        gfxdraw.aacircle(display.display, int(self.x), int(self.y), self.radius, RED)
        gfxdraw.aacircle(display.display, int(self.x2), int(self.y2), self.radius, GREEN)
        # draw.circle(display.display, RED, (int(self.x), int(self.y)), self.radius)
        # draw.circle(display.display, GREEN, (int(self.x2), int(self.y2)), self.radius)

        if self.condition:
            draw.line(display.display, BLACK, (self.x_1, 0), (self.x_1, display.height))
            draw.line(display.display, BLACK, (self.x_2, 0), (self.x_2, display.height))

        if self.critical_line:
            draw.aaline(display.display, BLUE, (self.x, self.y), (self.x2, self.y2))

        draw.aaline(display.display, BLACK, (self.x - 10, self.y - 10), (self.x + 10, self.y + 10))
        draw.aaline(display.display, BLACK, (self.x - 10, self.y + 10), (self.x + 10, self.y - 10))
        draw.aaline(display.display, BLACK, (self.x2 - 10, self.y2 - 10), (self.x2 + 10, self.y2 + 10))
        draw.aaline(display.display, BLACK, (self.x2 - 10, self.y2 + 10), (self.x2 + 10, self.y2 - 10))

import random
from math import hypot, sqrt, atan2, tau, cos, sin, pi
from typing import Optional

from pygame import gfxdraw, draw

from const import RED, GREEN, BLACK, BLUE
from display import Display
from object import Object, FPSCalculator
from util import animate, linear


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

        if self.fps_calculator:
            self.target_x = self.x
            self.target_x2 = self.x2
            self.target_y = self.y
            self.target_y2 = self.y2

        self.arc_x1 = 0
        self.arc_x2 = 0
        self.arc_y1 = 0
        self.arc_y2 = 0
        self.arc_vertices = list()
        self.arc_density = 24
        self.arc_condition = False

    def set_x2(self, x: int) -> 'Dualcircles':
        self.x2 = x
        return self

    def set_y2(self, y: int) -> 'Dualcircles':
        self.y2 = y
        return self

    def random_pos(self, display: Display) -> 'Dualcircles':
        """ Randomize the position of the circles. """

        if self.fps_calculator:
            self.target_x = random.randint(0, display.width)
            self.target_x2 = random.randint(0, display.width)
            self.target_y = random.randint(0, display.height)
            self.target_y2 = random.randint(0, display.height)
        else:
            self.x = random.randint(0, display.width)
            self.x2 = random.randint(0, display.width)
            self.y = random.randint(0, display.height)
            self.y2 = random.randint(0, display.height)
        return self

    def arc_y(self, x: float) -> float:
        return -(self.x2 - self.x) / (self.y2 - self.y) * (x - (self.x + self.x2) / 2) + (self.y + self.y2) / 2

    def tick(self):
        if self.fps_calculator:
            self.x = animate(self.x, self.target_x, self.fps_calculator.fps)
            self.x2 = animate(self.x2, self.target_x2, self.fps_calculator.fps)
            self.y = animate(self.y, self.target_y, self.fps_calculator.fps)
            self.y2 = animate(self.y2, self.target_y2, self.fps_calculator.fps)

        self.arc_condition = hypot(self.x - self.x2, self.y - self.y2) < self.radius * 2 and self.y != self.y2
        if self.arc_condition:
            self.tick_arc()
        else:
            self.arc_vertices.clear()

    def tick_arc(self):
        """ Calculates the overlapping arc between the two circles """

        a = self.x**2 - 2*self.x*self.x2 + self.x2**2 + self.y**2 - 2*self.y*self.y2 + self.y2**2
        b = -self.x**3 + self.x**2*self.x2 + self.x*self.x2**2 - self.x*self.y**2 + 2*self.x*self.y*self.y2 \
            - self.x*self.y2**2 - self.x2**3 - self.x2*self.y**2 + 2*self.x2*self.y*self.y2 - self.x2*self.y2**2
        d = -(self.y-self.y2)**2 * a * (a - 4*self.radius**2)

        self.arc_x1 = (-b + sqrt(d)) / (2 * a)
        self.arc_x2 = (-b - sqrt(d)) / (2 * a)

        self.arc_y1 = self.arc_y(self.arc_x1)
        self.arc_y2 = self.arc_y(self.arc_x2)

        # a - x
        theta_1 = atan2(self.arc_y2 - self.y, self.arc_x2 - self.x)
        theta_2 = atan2(self.arc_y1 - self.y, self.arc_x1 - self.x)
        theta_3 = atan2(self.arc_y1 - self.y2, self.arc_x1 - self.x2)
        theta_4 = atan2(self.arc_y2 - self.y2, self.arc_x2 - self.x2)

        theta_1, theta_2 = min(theta_1, theta_2), max(theta_1, theta_2)
        theta_3, theta_4 = min(theta_3, theta_4), max(theta_3, theta_4)

        if theta_2 - theta_1 > pi:
            theta_1, theta_2 = theta_2 - tau, theta_1
        if theta_4 - theta_3 > pi:
            theta_3, theta_4 = theta_4 - tau, theta_3

        self.arc_vertices.clear()
        radius = self.radius + 1
        # noinspection DuplicatedCode
        for theta in map(lambda x: linear(x, 0, self.arc_density, theta_1, theta_2), range(self.arc_density)):
            dx = cos(theta) * radius
            dy = sin(theta) * radius
            self.arc_vertices.append((self.x + dx, self.y + dy))
        # noinspection DuplicatedCode
        for theta in map(lambda x: linear(x, 0, self.arc_density, theta_3, theta_4), range(self.arc_density)):
            dx = cos(theta) * radius
            dy = sin(theta) * radius
            self.arc_vertices.append((self.x2 + dx, self.y2 + dy))

    # noinspection DuplicatedCode
    def render(self, display: Display):
        draw.circle(display.display, RED, (int(self.x), int(self.y)), self.radius)
        draw.circle(display.display, GREEN, (int(self.x2), int(self.y2)), self.radius)

        if self.arc_condition:
            gfxdraw.filled_polygon(display.display, self.arc_vertices, BLUE)

        draw.aaline(display.display, BLACK, (self.x - 10, self.y - 10), (self.x + 10, self.y + 10))
        draw.aaline(display.display, BLACK, (self.x - 10, self.y + 10), (self.x + 10, self.y - 10))
        draw.aaline(display.display, BLACK, (self.x2 - 10, self.y2 - 10), (self.x2 + 10, self.y2 + 10))
        draw.aaline(display.display, BLACK, (self.x2 - 10, self.y2 + 10), (self.x2 + 10, self.y2 - 10))

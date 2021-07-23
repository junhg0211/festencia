from random import random

from const import PRETENDARD_BOLD, BLACK, GREEN
from display import Display
from manager import MouseManager
from object import Text
from object.piste import Piste
from state import State
from util import Face, linear, limit


class Game(State):
    def __init__(self, title: str, host_name: str, display: Display, mouse_manager: MouseManager, state_manager):
        super().__init__()

        self.display = display
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.piste = Piste(host_name, '*VACANT*', display)

        title_face = Face(PRETENDARD_BOLD, 24, BLACK)
        self.title = Text(title, title_face, y=10).center_x(self.display)
        self.object_manager.add(self.title)

    def tick(self):
        super().tick()

        x_ = limit(self.mouse_manager.x, self.piste.x, self.piste.x + self.piste.width)
        y_ = limit(self.mouse_manager.y, self.piste.y, self.piste.y + self.piste.height)
        self.mouse_manager.set_pos(x_, y_)
        x = linear(self.mouse_manager.x, self.piste.x, self.piste.x + self.piste.width, 0, Piste.WIDTH)
        y = linear(self.mouse_manager.y, self.piste.y, self.piste.y + self.piste.height, 0, Piste.HEIGHT)
        self.piste.set_green_pos(x, y)

        self.piste.tick()

        if self.mouse_manager.left_start:
            self.piste.set_red_pos(random() * Piste.WIDTH, random() * Piste.HEIGHT)
            self.piste.click(x_, y_, GREEN)

    def render(self, display: Display):
        super().render(display)
        self.piste.render(display)

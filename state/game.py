from random import random

from const import PRETENDARD_BOLD, BLACK
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
        self.object_manager.add(self.piste)

        title_face = Face(PRETENDARD_BOLD, 24, BLACK)
        self.title = Text(title, title_face, y=10).center_x(self.display)
        self.object_manager.add(self.title)

    def tick(self):
        super().tick()

        if self.mouse_manager.left_start:
            self.piste.set_red_pos(random() * Piste.WIDTH, random() * Piste.HEIGHT)

        x = limit(self.mouse_manager.x, self.piste.x, self.piste.x + self.piste.width)
        y = limit(self.mouse_manager.y, self.piste.y, self.piste.y + self.piste.height)

        self.mouse_manager.set_pos(x, y)

        x = linear(self.mouse_manager.x, self.piste.x, self.piste.x + self.piste.width, 0, Piste.WIDTH)
        y = linear(self.mouse_manager.y, self.piste.y, self.piste.y + self.piste.height, 0, Piste.HEIGHT)
        self.piste.set_green_pos(x, y)

    def render(self, display: Display):
        super().render(display)

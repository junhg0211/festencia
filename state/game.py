from random import random
from threading import Thread

import globals
from const import PRETENDARD_BOLD, BLACK, GREEN
from display import Display
from manager import MouseManager
from object import Text
from object.piste import Piste
from state import State
from util import Face, linear, limit
from web.client import Client
from web.server import Server


class Game(State):
    HOST = 'host'

    def __init__(self, mode: str, display: Display, mouse_manager: MouseManager, state_manager, *,
                 title: str = '', host: str = '', port: int = 0, name: str = ''):
        super().__init__()

        self.mode = mode
        self.display = display
        self.mouse_manager = mouse_manager
        self.state_manager = state_manager

        self.piste = Piste('*VACANT*', '*VACANT*', '*UNTITLED*', display)

        if mode == Game.HOST:
            self.server = Server(port)
            self.thread = Thread(target=self.server.start)
            self.thread.setDaemon(True)
            self.thread.start()
            globals.data['server'] = self.server

        self.client = Client(host, port, self.state_manager, self.piste)
        self.client.start()

        if mode == Game.HOST:
            self.client.send_host(name)
            self.client.send_set_title(title)

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

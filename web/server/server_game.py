from math import hypot
from random import random
from threading import Thread
from time import sleep

from util import Log


class ServerGame:
    WIDTH = 20
    HEIGHT = 11
    RADIUS = 1.5

    SIGN_ENGARDE = 'engarde'
    SIGN_PRET = 'pret'
    SIGN_ALLEZ = 'allez'
    SIGN_HALTE = 'halte'

    STATE_WAITING = 0
    STATE_ENGARDE = 1
    STATE_PRET1 = 2
    STATE_PRET2 = 3
    STATE_ALLEZ = 4
    STATE_HALTE = 5
    STATE_HALTE_REST = 6
    STATE_RESULT = 7
    STATE_HALTE_LEFT = 9

    def __init__(self, server):
        self.server = server

        self.title = ''

        self.host_x = 0
        self.host_y = 0
        self.joiner_x = ServerGame.WIDTH
        self.joiner_y = ServerGame.HEIGHT

        self.host_score = 0
        self.joiner_score = 0

        self.assaut = 1
        self.time = 180.0
        self.state = 0
        """
        0 - not started waiting for participant
        1 - en garde
        2 - prêt (waiting for a second)
        3 - prêt (waiting for less than a second)
        4 - allez
        5 - halte (coup)
        6 - halte (8 score resting (30s))
        7 - end (result)
        9 - halte (participants left)
        """

        self.running = False
        self.thread = Thread(target=self.run)
        self.thread.setDaemon(True)

        self.frame_duration = 1/20

        self.delta = 0

    def collide(self) -> bool:
        return hypot(self.host_x - self.joiner_x, self.host_y - self.joiner_y) < ServerGame.RADIUS

    def host_click(self):
        self.server.announce(f'CLICK True {self.host_x} {self.host_y}')
        if self.collide():
            self.host_score += 1
            self.update_state(ServerGame.STATE_ALLEZ)

    def joiner_click(self):
        self.server.announce(f'CLICK False {self.joiner_x} {self.joiner_y}')
        if self.collide():
            self.joiner_score += 1
            self.update_state(ServerGame.STATE_ALLEZ)

    def start(self):
        self.running = True
        self.thread.start()

    def sign(self, sign: str):
        self.server.announce(f'ANNOUNCE {sign}')

    def check_engarde(self) -> bool:
        host_engarde = hypot(self.host_x, self.host_y) < ServerGame.RADIUS
        joiner_engarde = hypot(self.joiner_x - ServerGame.WIDTH,
                               self.joiner_y - ServerGame.HEIGHT) < ServerGame.RADIUS
        return host_engarde and joiner_engarde

    def update_state(self, state: int):
        Log.server(f'GAME State updated into {state}')
        self.state = state
        if self.state == ServerGame.STATE_ENGARDE:
            self.sign(ServerGame.SIGN_ENGARDE)
        elif self.state == ServerGame.STATE_PRET1:
            self.sign(ServerGame.SIGN_PRET)
        elif self.state == ServerGame.STATE_PRET2:
            self.delta = random()
        elif self.state == ServerGame.STATE_ALLEZ:
            self.delta = 5
            self.sign(ServerGame.SIGN_ALLEZ)
        elif self.state == ServerGame.STATE_HALTE_REST:
            self.delta = 30

    def run(self):
        while self.running:
            if self.state == ServerGame.STATE_WAITING:
                if self.server.joiner is not None:
                    self.update_state(ServerGame.STATE_ENGARDE)

            elif self.state == ServerGame.STATE_ENGARDE:
                if self.check_engarde():
                    self.update_state(ServerGame.STATE_PRET1)

            elif self.state == ServerGame.STATE_PRET1:
                if not self.check_engarde():
                    self.update_state(ServerGame.STATE_ENGARDE)
                self.delta += self.frame_duration
                if self.delta >= 1:
                    self.update_state(ServerGame.STATE_PRET2)

            elif self.state == ServerGame.STATE_ALLEZ:
                self.time -= self.frame_duration
                if self.time <= 0:
                    self.assaut += 1
                    if self.assaut == 3:
                        self.update_state(ServerGame.STATE_RESULT)
                    else:
                        self.update_state(ServerGame.STATE_HALTE_REST)

            elif self.state == ServerGame.STATE_HALTE:
                self.delta -= self.frame_duration
                if self.delta <= 0:
                    self.update_state(ServerGame.STATE_ENGARDE)

            elif self.state == ServerGame.STATE_HALTE_REST:
                self.delta -= self.frame_duration
                if self.delta <= 0:
                    self.update_state(ServerGame.STATE_ENGARDE)

            # elif self.state == ServerGame.STATE_RESULT:
            #     pass

            sleep(self.frame_duration)

    def shutdown(self):
        self.running = False

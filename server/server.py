from socket import socket
from time import time
from typing import Optional, List

from server import ServerClient


class Server:
    def __init__(self, port: int):
        self.port = port

        self.s = socket()

        self.running = False

        self.host: Optional[ServerClient] = None
        self.joiner: Optional[ServerClient] = None
        self.spectators: List[ServerClient] = list()

        self.host_x = 0
        self.host_y = 0
        self.joiner_x = 20
        self.joiner_y = 11

        self.title = ''

        self.assaut = 1
        self.time = 180.0

    def announce(self, message: str):
        if self.host:
            self.host.send(message)
        if self.joiner:
            self.joiner.send(message)
        for spectator in self.spectators:
            spectator.send(message)

    def get_anchor_time(self):
        return time(), self.time

    def host_click(self):
        pass  # todo when host clicked

    def joiner_click(self):
        pass  # todo when joiner clicked

    def start(self):
        self.s.bind(('', self.port))
        self.s.listen()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            conn, addr = self.s.accept()
            client = ServerClient(conn, *addr)
            client.handle()

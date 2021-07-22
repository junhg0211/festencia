from socket import socket
from time import time
from typing import Optional, List

from server import ServerClient, ServerGame


class Server:
    def __init__(self, port: int):
        self.port = port

        self.s = socket()

        self.running = False

        self.host: Optional[ServerClient] = None
        self.joiner: Optional[ServerClient] = None
        self.spectators: List[ServerClient] = list()

        self.game = ServerGame(self)

    def announce(self, message: str):
        if self.host:
            self.host.send(message)
        if self.joiner:
            self.joiner.send(message)
        for spectator in self.spectators:
            spectator.send(message)

    def get_anchor_time(self):
        return time(), self.game.time

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

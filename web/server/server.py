from socket import socket
from time import time
from typing import Optional, List

from web.server import ServerClient, ServerGame
from util import Log


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

    def start(self):  # this runs in thread
        self.s.bind(('', self.port))
        self.s.listen()
        self.running = True
        Log.server(f'Server started at {self.host}:{self.port}')
        self.run()

    def run(self):
        while self.running:
            try:
                conn, addr = self.s.accept()
            except OSError:
                break
            client = ServerClient(self, conn, *addr)
            client.handle()
        self.shutdown()

    def shutdown(self):
        if self.running:
            Log.server('Shutting down...')
            self.running = False
            if self.game.running:
                self.game.shutdown()
            if self.host is not None:
                self.host.quit()
            if self.joiner is not None:
                self.joiner.quit()
            for spectator in self.spectators:
                spectator.quit()
            self.s.close()

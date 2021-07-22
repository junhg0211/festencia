from socket import socket

from server import ServerClient


class Server:
    def __init__(self, port: int):
        self.port = port

        self.s = socket()

        self.running = False

        self.host = None
        self.joiner = None
        self.spectators = list()

        self.title = ''

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

from threading import Thread


class ServerGame:
    WIDTH = 20
    HEIGHT = 11
    RADIUS = 1.5

    def __init__(self, server):
        self.server = server

        self.title = ''

        self.host_x = 0
        self.host_y = 0
        self.joiner_x = ServerGame.WIDTH
        self.joiner_y = ServerGame.HEIGHT

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
        self.thread = Thread(target=self.start)

    def host_click(self):
        self.server.announce(f'CLICK True {self.host_x} {self.host_y}')

    def joiner_click(self):
        self.server.announce(f'CLICK False {self.joiner_x} {self.joiner_y}')

    def start(self):
        self.running = True
        self.thread.setDaemon(True)
        self.thread.start()

    def run(self):
        while self.running:
            print('Game ticking')
